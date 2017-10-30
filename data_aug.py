# -*- coding: utf-8 -*-
"""
Created on Sun May 14 15:41:25 2017

@author: GM
"""
from PIL import Image
import numpy as np
import os
#import cv2
import random
h = 3000
bg_db = os.listdir('MERGED_BACKGROUND/')
random.shuffle(bg_db)
np.save('list_', bg_db)
for time in range(4):
  outfile = "D:/google_train/3000_dataset/test_3000_12000/"
  processfile = 'final_dataset/train/'
#for Iter in range(num_output):
  #b_img = 500 #Number of background images
  f_img = 300 #Number of cropped traffic light images
#Change the Image address accordingly when executing the program
  bbox = np.zeros(((f_img)*10,4),dtype = np.int)
  class_num = 0
  for folder in os.listdir(processfile):
    class_dir = processfile + str(folder) + '/'
    box_num = 0
    pic_num = 3000*(time)
    for picture in os.listdir(class_dir):
      pic_dir = class_dir + str(picture)
      foreground = Image.open(pic_dir).convert("RGBA")
      f_w,f_h  = foreground.size
      new_ht = 450
      new_wt = int(np.floor(new_ht * f_w / f_h))
      foreground = foreground.resize((new_wt,new_ht),Image.ANTIALIAS)
      b_w,b_h  = 3000,3000
      x = np.linspace(0.4,1.0,num = 10)
      for k in range(10):
        #s = x[random.randint(0,9)]
        foreground  = foreground.resize([int(np.floor(new_wt*x[k])),int(np.floor(new_ht*x[k]))])
        new_w,new_h = foreground.size
    #Placing the image
        #i = random.randint(1,b_img)
        sequence = time*33000 + pic_num + class_num*3000
        print(sequence)
        bg_dir = bg_db[sequence]
        background = Image.open('MERGED_BACKGROUND/' + str(bg_dir))
        box = (500,0,3500,3000)
        background = background.crop(box)
        coordinates_x = random.randint(0, b_w-new_w)
        if k == 0:
            coordinates_y = random.randint(1200,1300)
        if k == 1:
            coordinates_y = random.randint(1100,1200)
        if k == 2:
            coordinates_y = random.randint(1000,1100)
        if k == 3:
            coordinates_y = random.randint(900,1000)
        if k == 4:
            coordinates_y = random.randint(800,900)
        if k == 5:
            coordinates_y = random.randint(700,800)
        if k == 6:
            coordinates_y = random.randint(400,600)
        if k == 7:
            coordinates_y = random.randint(250,400)
        if k == 8:
            coordinates_y = random.randint(100,250)
        if k == 9:
            coordinates_y = random.randint(50,100)
            
        background.paste(foreground,(coordinates_x,coordinates_y),foreground)
        
        #background.show()
        background = background.resize((h,h),Image.ANTIALIAS)
        background.save(outfile + str(class_num) + '/' + 'CLASS' + str(class_num) + '_' + str(pic_num) +".jpg")
        pic_num += 1
        s = 1
        bbox[box_num,:] = ([int(np.floor(coordinates_x*s)),int(np.floor(coordinates_y*s)),int(np.floor((coordinates_x+new_w)*s)),int(np.floor((coordinates_y+new_h)*s))])
        box_num += 1
    np.save(outfile + str(class_num) + '/bbox_' + str(class_num) + '_' + str(time) + '_' + str(pic_num), bbox)
    class_num += 1
