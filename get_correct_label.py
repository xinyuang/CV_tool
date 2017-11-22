
import numpy as np
target = open('img_to_delete.txt','r')
delete_list = []
for i in range(573):
    delete_img = target.readline()
    delete_img = delete_img.strip()
    delete_num = delete_img.split('_')[1]
    delete_list.append(delete_num)

source = open('resized_30.txt','r')
all_lines = source.readlines() 
print(all_lines)
source.close()
lists = []
w = open('resized_30.txt','r')
for i in range(1917):
	line = w.readline()
	print(line)
	post_line = line.replace(',',' ').split()
	print(post_line[0])
	if post_line[0] in delete_list:
		all_lines.remove(line)
		with open("correct_label.txt", "w") as new_f:
			for label in all_lines: 
				new_f.write(label)
		#lists.append(line)
#print(lists)
#           all_lines.remove(line)

            #print(len(lists))
#print(lists[0])
#with open("file_name.txt", "r") as f:
#    lines = f.readlines() 
#    lines.remove("Line you want to delete\n")
#    with open("new_file.txt", "w") as new_f:
#        for line in lines:        
#            new_f.write(line)