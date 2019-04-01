# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 18:38:50 2019

@author: xinyu
"""
import os
import bz2
import shutil
        
src = '3-27-2019'
for filename in os.listdir(src):
#    print(filename)
    filepath = os.path.join(src, str(filename))
#    print(file)
    
    newfilepath = os.path.join(src, filename.split('.')[0],filename[0:-4])
    folder = os.path.join(src, filename.split('.')[0])
    if not os.path.exists(folder):
        os.makedirs(os.path.join(src, filename.split('.')[0]))
    with open(newfilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
        for data in iter(lambda : file.read(100 * 1024), b''):
            new_file.write(data)
    mv_file = os.path.join(src, filename.split('.')[0], filename)
    print(mv_file)
    print(filepath)
    if filepath.split('.')[-1] != 'bz2':
        continue
    shutil.move(filepath,mv_file)