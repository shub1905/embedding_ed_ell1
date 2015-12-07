# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:47:18 2015

@author: patanjali
"""

import os
import numpy
from matplotlib import pyplot
import pandas

#%% Plotting runtimes

data = pandas.read_csv('data_norm.time', delimiter='\t')

pyplot.figure(2)
pyplot.plot(data['dimension'], data['embedding time'],'r+')
pyplot.xlabel('Dimension')
pyplot.ylabel('Embedding time')
pyplot.savefig('Embedding_time.png')

pyplot.figure(3)
pyplot.plot(data['dimension'], data['l1 time'],'r+')
pyplot.xlabel('Dimension')
pyplot.ylabel('Time to calculate l1')
pyplot.savefig('l1.png')

pyplot.figure(4)
pyplot.plot(data['dimension'], data['edit_time'],'r+')
pyplot.xlabel('Dimension')
pyplot.ylabel('Time to calculate edit distance')
pyplot.savefig('edit.png')

pyplot.figure(5)
pyplot.plot(data['l1 time'], data['edit_time'],'r+')
pyplot.xlabel('Time to calculate l1 distance')
pyplot.ylabel('Time to calculate edit distance')
pyplot.savefig('edit_vs_l1.png')

#%% Plotting distortions
time_dict = {}

for files in os.listdir('distances/'):
    file_name = 'distances/{}'.format(files)
    dist = numpy.load(file_name)
    params = file_name[:-9].split('_')
    if len(params) >= 5:
        [size, dimension, delta] = map(float, params[2:5])
        if dimension <= 20 and size > 2**dimension:
            size = 2**dimension
        if 'arr_1' in dist.keys():
            temp = dist['arr_1'].tolist()
            time_dict[files] = temp
            norm_factor = size * (size - 1) / 2