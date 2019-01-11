#! /usr/bin/python
from __future__ import division
from __future__ import print_function
import smbus
import math
import time
import can
import os
from gps import *
import threading
import thread
import datetime
import sys
from multiprocessing import Process, Lock, Value, Queue
from datetime import datetime
from time import mktime
from time import gmtime, strptime
from ctypes import c_char_p
from mtk import *
import mtk
import serial
# set CAN conversion parameters
# v2.2 corrects the output of IMU and increase the GPS update rate

gyro_offset = -250
accel_offset = -320
angle_offset = -250
gps_offset = -210
alt_offset = -2500
speed_offset = 0
sats_offset = 0

gyro_factor = 1/128
accel_factor = 0.01
angle_factor = 1/32768
gps_factor = 0.0000001
alt_factor = 0.125
speed_factor = 1/256
sats_factor = 1

# set GPS update rate tp 5 Hz
gps_freq = 5

gyro_id = int('0xCF02A80', 16)   #ARI_RP  yaw pitch
accel_id = int('0x8F02D80',16)   #ACCS_RP acc x y z
angle_id = int('0xCF02980', 16)  #SSI2_RP angle x y 
gps_id = int('0x18FEF380', 16)   #VP_RP   position
vds_id = int('0x18FEE880',16)    #VDS_RP  altiude + speed
sats_id = int('0x18FBF680', 16)  #VP2_RP  sats number

data_log_path = "/home/pi/traxen/can_gps/can_test/logged_data/"
queue_size = 500
file_size = 100000000
check_time = 300
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


def read_byte(adr):
  return bus.read_byte_data(address, adr)

def read_word(adr):
  high = bus.read_byte_data(address, adr)
  low = bus.read_byte_data(address, adr+1)
  val = (high << 8) + low
  return val

# read from address IMU pin
def read_word_2c(adr):
  val = read_word(adr)
  if (val >= 0x8000):
    return -((65535 - val) + 1)
  else:
    return val

def dist(a,b):
  return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
  radians = math.atan2(x, dist(y,z))
  return -math.degrees(radians)

def get_x_rotation(x,y,z):
  radians = math.atan2(y, dist(x,z))
  return math.degrees(radians)

# convert physical value to raw value
def real2raw(real, offset, factor, form):
    if real != real: return format(0xffffffff,'#10x')
    return format(int((real - offset) / factor), form)


def dump_queue(queue_size, dump_queue, glb_queue):

    if dump_queue.qsize() > queue_size:
        #print(time.time() - g_start.value)
        with glb_queue.get_lock():
            #change the working queue
            glb_queue.value = bytes((int(glb_queue.value) + 1) % 2)
        
        file_lock.acquire()
        file_name = get_file_name(g_file)
        with open(data_log_path + file_name, 'a') as f:
            while not dump_queue.empty():                               
                logged_data = dump_queue.get() 
                f.write(logged_data)
        file_lock.release()

                                    

def file_check(item,file_lock, lock,g_start, g_file, queue_list, glb_queue):
    while True:       
        #print(item)       
        lock.acquire()
        file_name = get_file_name(g_file)
        if os.path.getsize(data_log_path + file_name) > file_size:
            dump_queue(0, queue_list[int(glb_queue.value)], glb_queue)
            os.rename(data_log_path + file_name, data_log_path + "complete_" + file_name)
            time.sleep(0.2)
            file_name = time.strftime("GPS_%m-%d-%Y-%H-%M-%S.asc")
            with open(data_log_path + file_name, 'a') as f:
                f.write('date ' +  time.ctime() + '\r\n')
                f.write('base hex  timestamps absolute\r\n')
                f.write('internal events logged\r\n')
                f.write('// V 11.1.1 rPi version 2.1\r\n')
                f.write('Begin Triggerblock  ' +  time.ctime() + '\r\n')
                
                start = time.time()
                end = time.time()
                f.write("   {0:.6f}".format(end - start)+ ' Start of measurement\r\n')                  
                with g_file.get_lock():
                    g_file.value = get_file_time(file_name)
                with g_start.get_lock():
                    g_start.value = start 
        lock.release()

        dump_queue(queue_size, queue_list[int(glb_queue.value)], glb_queue)

            
def log_ecu(item,lock, queue_list, glb_queue):   
    while True:
        #print(item)
        msg = can_bus.recv()
        data = list(msg.data)
                
        channel = " 1 "
        msg_id = format(msg.arbitration_id, "#10x").upper()[2:].replace('X',' ') + 'x' + " Tx d " + str(msg.dlc) + " "
        strs = ''.join(' ' + format(e, '#04x')[2:].upper() for e in data)
        
        lock.acquire()
        start = g_start.value
        end = time.time()
        timeStamp = "   {0:.6f}".format(end - start)
        if end - start > 0:
            queue_list[int(glb_queue.value)].put(timeStamp + channel + msg_id + strs + '\r\n', False)
        lock.release()
        

def send_gps(item,gps_id, gps_offset, gps_factor, can_bus, lock, queue_list, glb_queue):
      # read and send GPS signal
      gpsp.start() # start it up
      while True:
          #print(item)
          latitude_real = gpsd.fix.latitude
          longitude_real = gpsd.fix.longitude
          raw_latitude = real2raw(latitude_real, gps_offset, gps_factor, '#10x')
          raw_longitude = real2raw(longitude_real, gps_offset, gps_factor, '#10x')
          data=[int(raw_latitude[8:10], 16),
                int(raw_latitude[6:8], 16),
                int(raw_latitude[4:6], 16),
                int(raw_latitude[2:4], 16),
                int(raw_longitude[8:10], 16),
                int(raw_longitude[6:8], 16),
                int(raw_longitude[4:6], 16),
                int(raw_longitude[2:4], 16)]
          msg = can.Message(arbitration_id=gps_id,
                                  data=data,
                                  extended_id=True)
          can_bus.send(msg)
          
          
          channel = " 1 "
          msg_id = format(gps_id, '#09x').upper()[2:] + 'x' + " Tx d 8 "
          strs = ''.join(' ' + format(e, '#04x')[2:].upper() for e in data)
          lock.acquire()         
          start = g_start.value
          end = time.time()
          timeStamp_GPS = "   {0:.6f}".format(end - start)
          if end - start > 0:
                queue_list[int(glb_queue.value)].put(timeStamp_GPS + channel + msg_id + strs + '\r\n', False)
          lock.release()
          
          speed_real = gpsd.fix.speed
          altitude_real = gpsd.fix.altitude
    
          raw_speed = real2raw(speed_real, speed_offset, speed_factor, '#06x')
          raw_altitude = real2raw(altitude_real, alt_offset, alt_factor, '#06x')
          vp2_data=[0xff,
                0xff,
                int(raw_speed[4:6], 16),
                int(raw_speed[2:4], 16),
                0xff,
                0xff,
                int(raw_altitude[4:6], 16),
                int(raw_altitude[2:4], 16)]
          msg = can.Message(arbitration_id=vds_id,
                                  data=vp2_data,
                                  extended_id=True)
          can_bus.send(msg)
          
          
          channel = " 1 "
          msg_id = format(vds_id, '#09x').upper()[2:] + 'x' + " Tx d 8 "
          strs = ''.join(' ' + format(e, '#04x')[2:].upper() for e in vp2_data)

          lock.acquire()         
          start = g_start.value
          end = time.time()
          file_name = get_file_name(g_file)
          timeStamp_GPS = "   {0:.6f}".format(end - start)
          if end - start > 0:
                queue_list[int(glb_queue.value)].put(timeStamp_GPS + channel + msg_id + strs + '\r\n', False)

          lock.release()
          
          sats_real = len(gpsd.satellites)

          raw_sats = real2raw(sats_real, sats_offset, sats_factor, '#04x')
          sats_data=[int(raw_sats[2:4], 16),
                0xff,
                0xff,
                0xff,
                0xff]
          msg = can.Message(arbitration_id=sats_id,
                                  data=sats_data,
                                  extended_id=True)
          can_bus.send(msg)
          
          
          channel = " 1 "
          msg_id = format(sats_id, '#09x').upper()[2:] + 'x' + " Tx d 5 "
          strs = ''.join(' ' + format(e, '#04x')[2:].upper() for e in sats_data)
          lock.acquire()         
          start = g_start.value
          end = time.time()
          file_name = get_file_name(g_file)
          timeStamp_GPS = "   {0:.6f}".format(end - start)
          if end - start > 0:
                queue_list[int(glb_queue.value)].put(timeStamp_GPS + channel + msg_id + strs + '\r\n', False)
          lock.release()
 
          time.sleep(0.1)

def send_imu(item, gyro_id, gyro_offset, gyro_factor, accel_id, \
             accel_offset, accel_factor, can_bus, lock, queue_list, glb_queue):
      # read and write gyro_x, y, z signal
      while True:
          #print(item)
          gyro_xout = -1 * read_word_2c(0x43)
          gyro_yout = -1 * read_word_2c(0x45)
          gyro_zout = -1 * read_word_2c(0x47)

          raw_gyro_xout = real2raw((gyro_xout / 131), gyro_offset, gyro_factor, '#06x')
          raw_gyro_yout = real2raw((gyro_yout / 131), gyro_offset, gyro_factor, '#06x')
          raw_gyro_zout = real2raw((gyro_zout / 131), gyro_offset, gyro_factor, '#06x')
          
          data=[int(raw_gyro_xout[4:6], 16),
                int(raw_gyro_xout[2:4], 16),
                int(raw_gyro_yout[4:6], 16),
                int(raw_gyro_yout[2:4], 16),
                int(raw_gyro_zout[4:6], 16),
                int(raw_gyro_zout[2:4], 16),
                0xff, 0xff]
          msg = can.Message(arbitration_id=gyro_id,
                                  data=data,
                                  extended_id=True)
          can_bus.send(msg)
          

          channel = " 1  "
          msg_id1 = format(gyro_id, '#09x').upper()[2:] + 'x' + " Tx d 8 "
          strs1 = ''.join(' ' + format(e, '#04x')[2:].upper()  for e in data)

          
          lock.acquire()
          start = g_start.value
          end1 = time.time()
          timeStamp1 = "   {0:.6f}".format(end1 - start)
          if end1 - start > 0:
                queue_list[int(glb_queue.value)].put(timeStamp1 + channel + msg_id1 + strs1 + '\r\n', False)
          lock.release()
          # read and send accel_x, y, z signal
          accel_xout = -1 * read_word_2c(0x3b)
          accel_yout = -1 * read_word_2c(0x3d)
          accel_zout = -1 * read_word_2c(0x3f)
          accel_xout_scaled = accel_xout / 16384.0
          accel_yout_scaled = accel_yout / 16384.0
          accel_zout_scaled = accel_zout / 16384.0
         
          raw_accel_xout = real2raw(accel_xout_scaled, accel_offset, accel_factor, '#06x')
          raw_accel_yout = real2raw(accel_yout_scaled, accel_offset, accel_factor, '#06x')
          raw_accel_zout = real2raw(accel_zout_scaled, accel_offset, accel_factor, '#06x')
          
          data=[int(raw_accel_xout[4:6], 16),
                int(raw_accel_xout[2:4], 16),
                int(raw_accel_yout[4:6], 16),
                int(raw_accel_yout[2:4], 16),
                int(raw_accel_zout[4:6], 16),
                int(raw_accel_zout[2:4], 16),
                0xff, 0xff]
          msg = can.Message(arbitration_id=accel_id,
                                  data=data,
                                  extended_id=True)
          can_bus.send(msg)
          
          
          channel = " 1  "
          msg_id2 = format(accel_id, '#09x').upper()[2:] + 'x' + " Tx d 8 "
          strs2 = ''.join(' ' + format(e, '#04x')[2:].upper()  for e in data)
          
          lock.acquire()
          start = g_start.value
          end2 = time.time()
          timeStamp2 = "   {0:.6f}".format(end2 - start)
          if end2 - start > 0:
                queue_list[int(glb_queue.value)].put(timeStamp2 + channel + msg_id2 + strs2 + '\r\n', False)
          lock.release()
          # read and send x,y angle signal
          x_angle = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
          y_angle = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
          
          raw_angle_xout = real2raw(x_angle, angle_offset, angle_factor, '#08x')
          raw_angle_yout = real2raw(y_angle, angle_offset, angle_factor, '#08x')
          
          data=[int(raw_angle_xout[6:8], 16),
                int(raw_angle_xout[4:6], 16),
                int(raw_angle_xout[2:4], 16),
                int(raw_angle_yout[6:8], 16),
                int(raw_angle_yout[4:6], 16),
                int(raw_angle_yout[2:4], 16),
                0xff, 0xff]
          msg = can.Message(arbitration_id=angle_id,
                                  data=data,
                                  extended_id=True)
          can_bus.send(msg)
          
          
          channel = " 1  "
          msg_id3 = format(angle_id, '#09x').upper()[2:] + 'x' + " Tx d 8 "
          strs3 = ''.join(' ' + format(e, '#04x')[2:].upper()  for e in data)
          
          lock.acquire()
          start = g_start.value
          end3 = time.time()
          timeStamp3 = "   {0:.6f}".format(end3 - start)
          if end1 - start > 0:
                queue_list[int(glb_queue.value)].put(timeStamp3 + channel + msg_id3 + strs3 + '\r\n', False)
          lock.release()
          time.sleep(0.01)


# initiate CAN bus
can_bus = can.interface.Bus(channel='can0', bustype='socketcan_ctypes')


bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68 # This is the address value read via the i2cdetect command
INT_PIN_CFG = 0x37
INT_ENABLE  = 0x38

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)
bus.write_byte_data(address, INT_PIN_CFG, 0x02)
bus.write_byte_data(address, INT_ENABLE, 0x01)

# set up GPS baud rate and update rate
def setupGPS():
    uart = serial.Serial(port = '/dev/ttyS0',baudrate=115200)
    #set GPS baud rate 115200
    baud = 115200
    set_baud = str.encode(mtk.update_baudrate(baud))
    print(set_baud)
    uart.write(set_baud)
    #set GPS update rate to 5 Hz
    update_rate = str.encode(mtk.update_nmea_rate(gps_freq))
    print(update_rate)
    for i in range(10):
        uart.write(update_rate)
        for j in range(10):
            result = uart.readline()
            if result:
                if str(result)[:8] == '$PMTK001' and str(result)[-4] == '3':
                    print('Command Succeded:', result)
                    break
        if j < 10: break
    uart.close()



gpsd = None #seting the global variable

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
def is_complete(file):
    status = file.split('.')[0].split('_')[0]
    if status == "complete":
        return True
    else:
        return False

def get_file_time(file_name):
    file_time = file_name.split('.')[0].split('_')[1]
    old = time.strptime(file_time,'%m-%d-%Y-%H-%M-%S')
    file_time = mktime(old)
    return file_time

def get_file_name(g_file):
    date = datetime.fromtimestamp(g_file.value).strftime("%m-%d-%Y-%H-%M-%S")
    return "GPS_" + date + ".asc"


if __name__ == '__main__':
  setupGPS()
  file_lock = Lock()
  lock = Lock()
  for data in os.listdir(data_log_path):
      lock.acquire()
      os.rename(data_log_path + data, data_log_path + "complete_" + data)
      lock.release()

  gpsp = GpsPoller() # create the thread
  queue_list = [Queue(601), Queue(601)] # initiate an array of Queue
  
  file_name = time.strftime("GPS_%m-%d-%Y-%H-%M-%S.asc")
  with open(data_log_path + file_name, 'a') as f:
    f.write('date ' +  time.ctime() + '\r\n')
    f.write('base hex  timestamps absolute\r\n')
    f.write('internal events logged\r\n')
    f.write('// V 11.1.1 rPi version 2.2\r\n')
    f.write('Begin Triggerblock  ' +  time.ctime() + '\r\n')
    start = time.time()
    end = time.time()
    f.write("   {0:.6f}".format(end - start)+ ' Start of measurement\r\n')                  

  g_start = Value('d', start)
  file_time = get_file_time(file_name)
  g_file = Value('d', file_time)
  glb_queue = Value('c', b'1')
    
  try: 
      
      fcheck = Process(target=file_check, args=("check",file_lock, lock, g_start, g_file, queue_list, glb_queue))
      fcheck.start()
      gps = Process(target=send_gps, args=("gps",gps_id, gps_offset, gps_factor, can_bus, lock, queue_list, glb_queue))     #gpsThread("test", 1)
      gps.start()
      imu = Process(target=send_imu, args=("imu", gyro_id, gyro_offset, gyro_factor, accel_id, \
                 accel_offset, accel_factor, can_bus, lock,queue_list, glb_queue))
      imu.start()
      ecu = Process(target=log_ecu, args=("ecu",lock, queue_list, glb_queue)) #ecuThread("ecu",3)
      ecu.start()
    
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    gpsp.running = False
    print ("Done.\nExiting.")
    sys.exit()

