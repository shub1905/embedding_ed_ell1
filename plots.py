# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:47:18 2015

@author: patanjali
"""

import os
import numpy
from matplotlib import pyplot
import pandas
import math

RESULTS_DIR = 'results/'

#%% Plotting runtimes

data = pandas.read_csv('data_norm.time', delimiter='\t')
new_arr = data[data['delta'] == 0.1]
max_d = int(max(new_arr['dimension']))
min_d = int(min(new_arr['dimension']))
a = range(min_d, max_d, 100)


pyplot.figure(2)
pyplot.plot(new_arr['dimension'], new_arr['embedding time'], 'r+', a, [x *
                                                                       math.log(x, 2) / 2**13 for x in a], 'b--', a, [x**2 * 1.0 / 2**25 for x in a], 'g--')
pyplot.xlabel('Dimension')
pyplot.ylabel('Embedding time')
pyplot.savefig(RESULTS_DIR + 'Embedding_time.png')


pyplot.figure(3)
pyplot.plot(data['dimension'], data['l1 time'], 'r+')
pyplot.xlabel('Dimension')
pyplot.ylabel('Time to calculate l1')
pyplot.savefig(RESULTS_DIR + 'l1.png')

pyplot.figure(4)
pyplot.plot(data['dimension'], data['edit_time'], 'r+')
pyplot.xlabel('Dimension')
pyplot.ylabel('Time to calculate edit distance')
pyplot.savefig(RESULTS_DIR + 'edit.png')

pyplot.figure(5)
pyplot.plot(data['l1 time'], data['edit_time'], 'r+')
pyplot.xlabel('Time to calculate l1 distance')
pyplot.ylabel('Time to calculate edit distance')
pyplot.savefig(RESULTS_DIR + 'edit_vs_l1.png')

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
        if 'arr_0' in dist.keys():
            data = dist['arr_0']
