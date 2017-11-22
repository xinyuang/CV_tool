import os

copy_folder =  '/media/xigu/DensoML/FER_2013_dataset/fer_data_public_test/'
new_folder = '/media/xigu/DensoML/FER_2013_dataset/fer_data_train/'
for file in os.listdir(copy_folder):
	print(file)
	if not os.path.exists(new_folder + str(file)):
		os.makedirs(new_folder + str(file))
