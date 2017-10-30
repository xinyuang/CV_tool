from PIL import Image
import numpy as np
import os
import random

folder = '/media/DensoML_lab/DensoML/emo/emo_test/'
new_folder = '/media/DensoML_lab/DensoML/emo/emo_class_160_test/'
move_number = 1400
h = 160
#for folder in range(11):
classes = os.listdir(folder)
for emotion in classes:
    if not os.path.exists(new_folder+ str(emotion)):
        os.makedirs(new_folder+ str(emotion))  
    for img in os.listdir(folder + emotion):
            print(img)
            foreground = Image.open(folder + emotion + '/' + str(img))
            foreground = foreground.resize((h,h),Image.ANTIALIAS)
            foreground.save(new_folder + emotion + '/' + str(img) + '.jpg')


  #random.shuffle(bg_db)
#   for i in range(move_number):
#     bg_pic = bg_db[i]
#     os.rename(move_from + str(folder) + '/' + str(bg_pic), move_to + str(folder) + '/' + str(bg_pic))





# import os
# from PIL import Image

# h = 299

# for i in range(11):
#   for images in os.listdir(str(i) + '/'):
   
#     foreground = Image.open(str(i) + '/' + str(images))
#     foreground = foreground.resize((h,h),Image.ANTIALIAS)
#     foreground.save(str(i) + '/' + str(images))
