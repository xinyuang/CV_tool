import os
from glob import glob
from subprocess import call


copy_folder =  '/media/xigu/DensoML/C3D_data/Train_AFEW/dropped_'
new_folder = '/media/xigu/DensoML/C3D_data/Train_AFEW/dropped_mp4'
for folder in os.listdir(copy_folder):
	print(folder)
	avi_path = os.path.join(copy_folder,folder, '*.avi')
	avi_files = glob(avi_path)
	for avi_file in avi_files:
		print(avi_file)
		mp4_file = os.path.join(new_folder, folder, avi_file.split('/')[-1].split('.')[0] + '.mp4')
		print(mp4_file)

		cmd = "avconv -i " + avi_file + ' -c:v libx264 -c:a copy ' +  mp4_file

		call(cmd, shell=True)