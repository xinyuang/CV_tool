import numpy as np
import argparse
import imutils
import cv2
from PIL import Image
import os
import random
foreground = Image.open("test"+".png").convert("RGBA")
background = Image.open("bg"+".jpg")
box = (500,0,3500,3000)
background = background.crop(box)


background.paste(foreground,(0,0),foreground)
background.save('CLASS10_IMG'+".jpg")