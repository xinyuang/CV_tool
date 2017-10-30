# -*- coding: utf-8 -*-
"""
Created on Sun May 14 20:04:08 2017

@author: GM
"""
import cv2
file_name = "image3.png"
src = cv2.imread(file_name, 1)
tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
_,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
b, g, r = cv2.split(src)
rgba = [b,g,r, alpha]
dst = cv2.merge(rgba,4)
cv2.imwrite("test2.png", dst)