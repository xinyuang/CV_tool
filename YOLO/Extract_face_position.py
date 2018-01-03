import csv
import glob
import os
import os.path
from subprocess import call

#from Ipython.core.debugger import Tracer

    
def process_each_folder(folder):
	#path = folder + '/'
	path = folder
	
	path_for_yolo = '/media/xigu/DensoML/xinyu/YOLO_mark/darknet/' #you need to change here
	cmd = "./darknet detector valid /media/xigu/DensoML/xinyu/YOLO_mark/darknet/face_yolo/yolo-only-face.data cfg/face.cfg face.weights  --threshold 0.3"



	list_file = open(path_for_yolo+'results/'+'test_list.txt','w') 

	for img in os.listdir(folder): 
		print(folder + str(img))
		img_name = folder + str(img)
		list_file.write(img_name + '\n')
	
	list_file.close()

	call(cmd, shell=True)

		
		## Process Result from YOLO 
	result = path_for_yolo+'results/'+'comp4_det_test_face.txt'   
	f = open(result, 'r')

	frames = {}
	for line in f.readlines():
		part = line.split(' ')
		index = part[0]
		score = part[1]
		position = '_'.join(part[2:6])
		if index not in frames.keys():
			frames[index] = [score,position]
		elif (score>frames[index][0]):
			frames[index] = [score,position]
	f.close()


	faces = path + '_face_position'
	f = open(faces, 'w')
	for index in frames.keys():
		position = frames[index][1]
		line = '\t'.join([index]+position.split('_'))
		f.write(line)
	f.close()


def main():
	#path = os.getcwd() + '/data/Drowsiness/Training_Dataset/*'
	# src = '/media/xigu/DensoML/xinyu/xinyu/binary_emotion/emo_test/'
	src = '/media/xigu/DensoML/xinyu/xinyu/binary_emotion/4_AffectNet/'
	# src =  '/media/xigu/DensoML/combination_data/whole_dataset/' #This is for multiple folders, so you need to change
	# subjects = glob.glob(src)  
	# print(subjects)
	#subjects = subjects[0:1] #For test
	#import ipdb; ipdb.set_trace()  #debug
	for subject in os.listdir(src):
		print(src + str(subject))
		folder = src + str(subject) + '/'
		process_each_folder(folder)


main()

