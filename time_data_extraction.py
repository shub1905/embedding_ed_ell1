import numpy
import os

time_dict = {}
data_file = open('data.time', 'w')
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
            str_to_write = '{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(size, dimension, delta, temp['embedding_time'], temp[
                                                                 'l1_distance_time'], temp['edit_distance_time'], temp['total_time'])
            data_file.write(str_to_write)


print [(x, time_dict[x]) for x in time_dict][0]
data_file.close()
