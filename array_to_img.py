from pandas import DataFrame, read_csv
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import json
import string
import cv2
from PIL import Image
size = 160, 160
file = r'fer2013.csv'
#file = r'simple_test.csv'
data_dir = 'fer_data/'
df = pd.read_csv(file)
index = df['emotion'][df['Usage'] == 'PublicTest'].index.tolist()
print(len(index))
num = 0
for i in index:
	classes = df.at[i,'emotion']
	s = "[" + df.at[i,'pixels'] + "]"
	new_s = s.replace(' ', ',')
	im_array = json.loads(new_s)
	img = np.array(im_array).reshape(48,48)
	im = Image.fromarray(img.astype(np.uint8))
	im = im.resize((size), Image.ANTIALIAS)
	im.save(data_dir + str(classes) + '/' + str(num) + '.png')
	num = num + 1










	# fig = plt.figure()
	# plt.imshow(img,cmap='gray')
	# plt.show()