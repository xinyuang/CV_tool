
from PIL import Image
h = 448
foreground = Image.open('0.jpg')
foreground = foreground.resize((h,h),Image.ANTIALIAS)
foreground.save('smallestCLASS.jpg')