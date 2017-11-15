# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 17:28:27 2017

@author: xinyu
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:28:59 2017

@author: xinyu
"""
from pygame import *
import pygame
import time
import cv2
import numpy as np
import pandas as pd
user_1_time = []
user_2_time = []
user_1_level = []
user_2_level = []
user_3_time = []
user_4_time = []
user_3_level = []
user_4_level = []
writer = pd.ExcelWriter('drose_data.xlsx', engine='xlsxwriter')
screen = display.set_mode((500,500))   # 1180, 216
start_time = time.time()
DONE = False
#keys = key.get_pressed() # It gets the states of all keyboard keys.
# Create a VideoCapture object
cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)
cap3 = cv2.VideoCapture(3)
# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
if (cap1.isOpened() == False): 
  print("Unable to read camera1 feed")
if (cap2.isOpened() == False): 
  print("Unable to read camera2 feed")
if (cap2.isOpened() == False): 
  print("Unable to read camera3 feed")
# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(5))
#frame_width1 = int(cap1.get(3))
#frame_height1 = int(cap1.get(4)) 
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('user1.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 30, (frame_width,frame_height))
out1 = cv2.VideoWriter('user2.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 30, (frame_width,frame_height))
out2 = cv2.VideoWriter('user3.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 30, (frame_width,frame_height))
out3 = cv2.VideoWriter('user4.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 30, (frame_width,frame_height))
while not DONE:
  ret, frame = cap.read()
  ret1, frame1 = cap1.read()
  ret2, frame2 = cap2.read()
  ret3, frame3 = cap3.read()
  if ret == True: 
    # Write the frame into the file 'output.avi'
    out.write(frame)
    out1.write(frame1)
    out2.write(frame2)
    out3.write(frame3)
    # Display the resulting frame    
    cv2.imshow('frame',frame)
    cv2.imshow('frame1',frame1)
    cv2.imshow('frame2',frame2)
    cv2.imshow('frame3',frame3)
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    
    for event in pygame.event.get():
         if event.type == pygame.QUIT: 
             #sys.exit()
             # When everything done, release the video capture and video write objects
             DONE = True
         elif (event.type == KEYDOWN):
            if ((event.key == K_ESCAPE)
                 or (event.key == K_q)):
                user1_t = pd.DataFrame({'time': user_1_time})
                user2_t = pd.DataFrame({'time': user_2_time})
                user3_t = pd.DataFrame({'time': user_3_time})
                user4_t = pd.DataFrame({'time': user_4_time})                
                user1_l = pd.DataFrame({'level': user_1_level})
                user2_l = pd.DataFrame({'level': user_2_level})
                user3_l = pd.DataFrame({'level': user_3_level})
                user4_l = pd.DataFrame({'level': user_4_level})                
                
                user1_t.to_excel(writer, sheet_name='user1')
                user1_l.to_excel(writer, sheet_name='user1',startcol=2, index=False)
                user2_t.to_excel(writer, sheet_name='user2')
                user2_l.to_excel(writer, sheet_name='user2',startcol=2, index=False)
                user3_t.to_excel(writer, sheet_name='user3')
                user3_l.to_excel(writer, sheet_name='user3',startcol=2, index=False)
                user4_t.to_excel(writer, sheet_name='user4')
                user4_l.to_excel(writer, sheet_name='user4',startcol=2, index=False)                
                writer.save()
                cap.release()
                cap1.release()
                cap2.release()
                cap3.release()
                out.release()
                out1.release()
                out2.release()
                out3.release()
                # Closes all the frames
                cv2.destroyAllWindows() 
                DONE = True
            if (event.key == K_KP1):
                #self.char_y = self.char_y - 10
                user_1_time.append((time.time() - start_time))
                user_1_level.append(1)
                print("%0.4f kp_1 down"%(time.time() - start_time))
            if (event.key == K_KP2):
                  #self.char_y = self.char_y + 10
                user_1_time.append((time.time() - start_time))
                user_1_level.append(2)
                print("%0.4f kp_2 down"%(time.time() - start_time))
            if (event.key == K_KP3):
                user_1_time.append((time.time() - start_time))
                user_1_level.append(3)
                print("%0.4f kp_3 down"%(time.time() - start_time))
                #self.char_x = self.char_x + 10
            
            if (event.key == K_a):
                #self.char_y = self.char_y - 10
                user_2_time.append((time.time() - start_time))
                user_2_level.append(1)
                print("%0.4f a down"%(time.time() - start_time))
            if (event.key == K_s):
                  #self.char_y = self.char_y + 10
                user_2_time.append((time.time() - start_time))
                user_2_level.append(2)
                print("%0.4f s down"%(time.time() - start_time))
            if (event.key == K_d):
                user_2_time.append((time.time() - start_time))
                user_2_level.append(3) 
                print("%0.4f d down"%(time.time() - start_time))

            if (event.key == K_b):
                #self.char_y = self.char_y - 10
                user_3_time.append((time.time() - start_time))
                user_3_level.append(1)
                print("%0.4f b down"%(time.time() - start_time))
            if (event.key == K_n):
                  #self.char_y = self.char_y + 10
                user_3_time.append((time.time() - start_time))
                user_3_level.append(2)
                print("%0.4f n down"%(time.time() - start_time))
            if (event.key == K_m):
                user_3_time.append((time.time() - start_time))
                user_3_level.append(3) 
                print("%0.4f m down"%(time.time() - start_time))


            if (event.key == K_KP4):
                #self.char_y = self.char_y - 10
                user_4_time.append((time.time() - start_time))
                user_4_level.append(1)
                print("%0.4f 4 down"%(time.time() - start_time))
            if (event.key == K_KP5):
                  #self.char_y = self.char_y + 10
                user_4_time.append((time.time() - start_time))
                user_4_level.append(2)
                print("%0.4f 5 down"%(time.time() - start_time))
            if (event.key == K_KP6):
                user_4_time.append((time.time() - start_time))
                user_4_level.append(3) 
                print("%0.4f 6 down"%(time.time() - start_time))                
                #self.char_x = self.char_x + 10
  # Break the loop
# =============================================================================
#   else:
#     break 
# =============================================================================
 



