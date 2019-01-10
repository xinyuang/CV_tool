# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 05:10:47 2019

@author: xinyu
"""

import os
import csv
import pandas as pd
import shutil

src = 'Machine Learning'
fieldnames = ['name']
csv_path = src + '\candidates.csv'
excel_path = src + '\candidates.xlsx'
number = 1
with open('candidates.csv', mode='w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for filename in os.listdir(src):
        filepath = os.path.join(src, str(filename))
        print(filepath)
        new_name = str(number) + "_" + filename
        target = os.path.join(src, new_name)
        print(new_name)
        os.rename(filepath, target)
        writer.writerow({'name': new_name})
        number += 1

df_new = pd.read_csv('candidates.csv')
writer = pd.ExcelWriter('candidates.xlsx')
df_new.to_excel(writer, index = False)
writer.save()
os.remove('candidates.csv')
shutil.move('candidates.xlsx', excel_path)
