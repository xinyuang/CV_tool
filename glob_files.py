# import os

# copy_folder =  '/media/xigu/DensoML/xinyu/MV3D/our_data/raw/kitti/2011_09_26/' 

# # new_folder = '/media/xigu/DensoML/combination_data/test_1000_per_class/'
# for file in os.listdir(copy_folder):
# 	print(copy_folder + str(file) + '/projection')
# 	if not os.path.exists(copy_folder + str(file) + '/projection/data'):
# 		os.makedirs(copy_folder + str(file) + '/projection/data')

import shutil
import os
import random
from glob import glob

# src = '/media/xigu/DensoML/combination_data/whole_dataset/'
des = '/media/xigu/DensoML/combination_data/test_1000_per_class/'
src = '/media/xigu/DensoML/xinyu/MV3D/our_data/raw/kitti/2011_09_26/' 
move_to = '/bboxes/data/'

for filename in os.listdir(src):
	d = {}
	# for img in os.listdir(src+'/'+str(filename)):
	# 	if filename[0] == '.':
	# 		continue
	# 	name = filename.split('_')[0]
	# 	if name not in d:
	# 		d[name] = [filename]
	# 	else:
	# 		d[name].append(img)
	des_path = os.path.join(src, str(filename))
	# print(des_path)
	box_file = des_path + '/bboxes'
	print(filename)
	path = os.path.join(src, box_file,'*_bbox.bin')
	files_path = glob(path)
	# print(files_path)
	# print(len(files_path))
	for move_file in files_path:
		print(move_file)
		print(type(move_file.split('/')[-1]))
		# des
		print(str(des_path) + move_to + str(move_file.split('/')[-1]))

		shutil.move(move_file, str(des_path) + move_to + str(move_file.split('/')[-1]))