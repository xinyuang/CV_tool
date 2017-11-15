# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 00:03:55 2017

@author: xinyu
"""

import cv2
import numpy as np
import math
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
# Create a VideoCapture object and read from input file   SampleVideo.mp4
# If the input is the camera, pass 0 instead of the video file name subject-G.avi
#process excel data
data = pd.read_excel('training-sheet_subject-G.xlsx', sheetname='sheet1')
cap = cv2.VideoCapture('./subject-G.avi')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(5))
# Check if camera opened successfullyq       avi form use  cv2.VideoWriter_fourcc('M','J','P','G')
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
out1 = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc(*'MP4V'), fps, (frame_width,frame_height)) 
#out2 = cv2.VideoWriter('outpy2.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 100, (frame_width,frame_height)) 
#out3 = cv2.VideoWriter('outpy3.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 100, (frame_width,frame_height)) 
#out4 = cv2.VideoWriter('outpy4.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 100, (frame_width,frame_height)) 


# Read until video is completed

count = 0
while(cap.isOpened()):
  # Capture frame-by-frame
  
  ret, frame = cap.read()
  count = count + 1
  if ret == True:
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    #cv2.imshow('Frame',frame)
    
    time = math.floor((count - 157)/60)
    minute = math.floor(time/60)
    second = time%60
    segment = math.floor(time/5)
    if segment <0:
        segment = 0
    cv2.putText(img = frame, text = 'current time:  ' + str(minute) + 'min  ' + str(second) + 'sec', org = (int(20),int(20)), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.7, 
                        color = (0, 255, 0))    
    cv2.putText(img = frame, text = 'segment:      ' + str(data['min'][segment]) + 'min  ' + str(data['sec'][segment]) + 'sec', org = (int(20),int(40)), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.7, 
                        color = (0, 255, 0))    
    cv2.putText(img = frame, text = 'teacher1:' + str(data['teacher 1'][segment]) + '   teacher2:' + str(data['teacher 2'][segment]), org = (int(20),int(frame_height) - 60), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.7, 
                        color = (0, 255, 0))
    cv2.putText(img = frame, text = 'average:'  , org = (int(20),int(frame_height) - 40), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.7, 
                        color = (0, 255, 0)) 
    cv2.putText(img = frame, text = '           '  + str(data['average'][segment]) , org = (int(20),int(frame_height) - 20), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 1, 
                        color = (0, 0, 255)) 
    #if minute < 15:     
    out1.write(frame)
    #elif minute >= 15 and minute < 30:
   #     out1.release()
   #     out2.write(frame)
  #  elif minute >= 30 and minute < 45:
  #      out2.release()
    #    out3.write(frame)
   # elif minute >= 45:
  #      out3.release()
  #      out4.write(frame)
    cv2.imshow('Frame',frame)
    
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
cap.release()
out1.release()
#out4.release()
# Closes all the frames
cv2.destroyAllWindows()