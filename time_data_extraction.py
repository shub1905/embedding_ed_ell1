from __future__ import division
import numpy
import os

time_dict = {}
data_file = open('data_norm.time', 'w')
data_file.write('size\tdimension\tdelta\tembedding time\tl1 time\tedit_time\ttotat time\n')
''' format = size, dimension, delta, embedding time, l1 time, edit_time, totat time'''

for files in os.listdir('distances/'):
    file_name = 'distances/{}'.format(files)
    dist = numpy.load(file_name)
    params = file_name[:-9].split('_')
    if len(params) == 5:
        [size, dimension, delta] = map(float, params[-3:])
        if 'arr_1' in dist.keys():
            temp = dist['arr_1'].tolist()
            time_dict[files] = temp
            norm_factor = size * (size - 1) / 2
            str_to_write = '{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(size, dimension, delta, temp['embedding_time'] / size, temp[
                                                                 'l1_distance_time'] / norm_factor, temp['edit_distance_time'] / norm_factor, temp['total_time'] / norm_factor)
            data_file.write(str_to_write)


print [(x, time_dict[x]) for x in time_dict][0]
data_file.close()
