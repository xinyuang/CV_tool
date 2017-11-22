# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 14:23:47 2017

@author: shiyoung
"""

from matplotlib import pyplot as plt
from pylab import ginput
import cv2
import numpy as np


with open('img_list.txt', 'r') as f:
    with open('lines.txt', 'a') as w:
        line = f.readline()
        while line != '':
            line = line.strip()
            w.write(line+'\n')
            img = cv2.imread(line)
            f1 = plt.figure(1)
            plt.imshow(img)
            print(img.shape[0])
            print(img.shape[1])
            plt.axis('image')
            for i in range(2):
                x = []
                y = []
                print("line {0}".format(i+1))
                for j in range(4):
                    point = ginput(1)
                    norm_x = point[0][0] / img.shape[1]
                    norm_y = point[0][1] / img.shape[0]
                    print(point)
                    print(norm_x)
                    print(norm_y)
                    x.append(point[0][0])
                    y.append(point[0][1])

                print("lengthX:{}".format(len(x)))
                print(x)
                print(y)
                coef_yx = np.polyfit(y, x, 4)

                # draw curve to check the correctness
                #fittedY = np.linspace(min(y), max(y), 200)
                #fittedX = np.polyval(coef_yx, fittedY)
                #f2 = plt.figure(1)
                #plt.xlim([0, img.shape[1]])
                #plt.ylim([0, img.shape[0]])
                #plt.scatter(x, y)
                #plt.plot(fittedX, fittedY)

                p1 = [np.poly1d(coef_yx)(1), 1]
                p2 = [np.poly1d(coef_yx)(min(y)), min(y)]
                print(p1, p2)
                coef = [str(abc) for abc in coef_yx]
                w.write(','.join(coef))
                w.write(',')
                w.write('{0},{1},'.format(p1[0], p1[1]))
                w.write('{0},{1}\n'.format(p2[0], p2[1]))
            plt.close()
            line = f.readline()


#filename = '1.jpg'
#img = cv2.imread(filename)
#print(img.shape)
#plt.imshow(img)
#plt.axis('image')
#[p1, p2] = ginput(2)
