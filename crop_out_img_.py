from pandas import DataFrame, read_csv
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import string
import os
import cv2
import glob

# data_folder =  '/media/xigu/DensoML/combination_data/test_1000_per_class' 
# des_folder =  '/media/xigu/DensoML/combination_data/croped_test_1000_per_class' 
data_folder = '/media/xigu/DensoML/VggFace2/test'
des_folder = '/media/xigu/DensoML/VggFace2/cropped_test' 

if not os.path.exists(os.path.dirname(des_folder)):
	os.makedirs(os.path.dirname(des_folder))

size = 160
no_face = 0
# file = r'dataFile_0001_new.csv'
for classes in os.listdir(data_folder):
	if classes[0] == '.':
		continue
	csv_path = os.path.join(data_folder,str(classes), "_face_position")
	print(csv_path)
	# os.remove(csv_path)

	df = pd.read_csv(csv_path, names = ['label'] )
	num_rows = len(df.index)
	
	for i in range(num_rows):
		# print(type(df.at[i,'label']))
		result = df.at[i,'label'].split()
		# print(result)
		image_name = os.path.join(data_folder,str(classes), result[0] + ".*")
		print(image_name)
		image_name = glob.glob(image_name)
		print(image_name)
		img = cv2.imread(image_name[0])
		# cv2.imshow('face', img)
		# cv2.waitKey(0)
		bbox = result[1:5]
		Area = (int(float(bbox[3])) - int(float(bbox[1])))*(int(float(bbox[2])) - int(float(bbox[0])))
		if Area < 8500:
			no_face = no_face + 1
			continue

		crop_img = img[int(float(bbox[1])):int(float(bbox[3])), int(float(bbox[0])):int(float(bbox[2]))]
		resized_image = cv2.resize(crop_img, (size, size)) 
		cropped_class = os.path.join(des_folder,str(classes))
		if not os.path.exists(cropped_class):
			os.makedirs(cropped_class)
		new_img_name = os.path.join(cropped_class, result[0] + ".jpg")
		print(new_img_name)
		cv2.imwrite(new_img_name,resized_image)

		# cv2.imshow('face', resized_image)
		# cv2.waitKey(0)
# cv2.destroyAllWindows()
print(no_face)





# img = cv2.imread("/media/xigu/DensoML/emotioNet/downloads/dataFile_0001/image0.jpg")
# crop_img = img[33:134, 52:125] # Crop from x, y, w, h -> 100, 200, 300, 400
# # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
# cv2.imshow("cropped", crop_img)
# cv2.waitKey(0)

