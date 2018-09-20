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
import time
import cv2
import numpy as np

start_time = time.time()
DONE = False
#keys = key.get_pressed() # It gets the states of all keyboard keys.
# Create a VideoCapture object
cap = cv2.VideoCapture(1)
# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(5))
#frame_width1 = int(cap1.get(3))
#frame_height1 = int(cap1.get(4)) 
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('user1.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 30, (frame_width,frame_height))
while not DONE:
  ret, frame = cap.read()
  if ret == True: 
    # Write the frame into the file 'output.avi'
    out.write(frame)
    # Display the resulting frame    
    cv2.imshow('frame',frame)
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
        cap.release()
        out.release()

        # Closes all the frames
        cv2.destroyAllWindows() 
        DONE = True

                #self.char_x = self.char_x + 10
  # Break the loop
# =============================================================================
#   else:
#     break 
# =============================================================================
