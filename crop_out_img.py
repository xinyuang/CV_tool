from pandas import DataFrame, read_csv
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import string
import os
import cv2

csv_folder = '/media/xigu/DensoML/emotioNet/new_csv/'
size = 160
i = 0
file = r'dataFile_0001_new.csv'


for file in os.listdir(csv_folder):
    if file[0] == '.':
        continue
	csv_path = csv_folder + str(file)
	df = pd.read_csv(csv_path)
	for i in range(len(df)):
	    s_bbox = df.at[i,'yolo_bbox']
	    if s_bbox != s_bbox:
	    	continue
	    s_AU = df.at[i,'1']
	    AU = s_AU.split()
	    label = [int(AU[0]), int(AU[1]), int(AU[3]), int(AU[4]), int(AU[5]), int(AU[8]), int(AU[11]),int(AU[14]), int(AU[16]), int(AU[19]), int(AU[24]), int(AU[25])]
	    print(label)
	    i = i + 1

		bbox = s_bbox.split(" ")
		file_name = df.at[0,'file_name']
		img = cv2.imread(file_name)
		crop_img = img[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

		resized_image = cv2.resize(crop_img, (size, size)) 
		cv2.imshow('face', resized_image)

		cv2.imwrite('newImage.png',resized_image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()





# img = cv2.imread("/media/xigu/DensoML/emotioNet/downloads/dataFile_0001/image0.jpg")
# crop_img = img[33:134, 52:125] # Crop from x, y, w, h -> 100, 200, 300, 400
# # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
# cv2.imshow("cropped", crop_img)
# cv2.waitKey(0)


# size = 160, 160
# file = r'fer2013.csv'
# #file = r'simple_test.csv'
# data_dir = 'fer_data/'
# df = pd.read_csv(file)
# index = df['emotion'][df['Usage'] == 'PublicTest'].index.tolist()
# print(len(index))
# num = 0
# for i in index:
# 	classes = df.at[i,'emotion']
# 	s = "[" + df.at[i,'pixels'] + "]"
# 	new_s = s.replace(' ', ',')
# 	im_array = json.loads(new_s)
# 	img = np.array(im_array).reshape(48,48)
# 	im = Image.fromarray(img.astype(np.uint8))
# 	im = im.resize((size), Image.ANTIALIAS)
# 	im.save(data_dir + str(classes) + '/' + str(num) + '.png')
# 	num = num + 1

#new_s = s_bbox.replace(' ', ',')