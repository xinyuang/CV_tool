import shutil
import os
import random

src = 'emo_class_160'
des = 'emo_class_160_vali'


for filename in os.listdir(src):
	d = {}
	for img in os.listdir(src+'/'+str(filename)):
		if filename[0] == '.':
			continue
		name = filename.split('_')[0]
		if name not in d:
			d[name] = [filename]
		else:
			d[name].append(img)
	print(len(d[name]))

	for name in d:
		num = len(d[name])
		draft = num//10
		print(draft)
		random.shuffle(d[name])
		for name in d[name][0:draft]:
			print(src+'/'+filename + '/' + name)
			# shutil.move(src+'/'+filename + '/' + name, des+'/'+filename+ '/' + name)