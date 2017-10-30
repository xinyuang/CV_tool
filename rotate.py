# -*- coding: utf-8 -*-
"""
Created on Sun May 14 19:18:34 2017

@author: GM
"""

from PIL import Image
# open an image file (.bmp,.jpg,.png,.gif)
# change image filename to something you have in the working folder
im1 = Image.open("image3.png")
# rotate 60 degrees counter-clockwise
im2 = im1.rotate(60)
# brings up the modified image in a viewer, simply saves the image as
# a bitmap to a temporary file and calls viewer associated with .bmp
# make certain you have an image viewer associated with this file type
im2.show()
# save the rotated image as d.gif to the working folder
# you can save in several different image formats, try d.jpg or d.png 
# PIL is pretty powerful stuff and figures it out from the extension
im2.save("d.png")