from __future__ import division
import numpy
import os
import common
from optparse import OptionParser


def generate_time_file(include, exclude, file_name='data_norm.time'):
    files_list = common.get_file_names(include, exclude)
    time_dict = {}
    data_file = open(file_name, 'w')
    data_file.write('size\tdimension\tdelta\tembedding time\tl1 time\tedit_time\ttotal time\n')
    ''' format = size, dimension, delta, embedding time, l1 time, edit_time, total time'''

    for files in files_list:
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
                str_to_write = '{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(size, dimension, delta, temp['embedding_time'] / size, temp[
                                                                     'l1_distance_time'] / norm_factor, temp['edit_distance_time'] / norm_factor, temp['total_time'] / norm_factor)
                data_file.write(str_to_write)

    data_file.close()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-e", "--exclude", dest="exclude", action='append',
                      help='exclude all files matching these regex')
    parser.add_option("-i", "--include", dest="include", action='append',
                      help='include files matching all of these regex')
    parser.add_option("-f", "--file", dest="file_name",
                      default='data_norm.time', help='write stats to this file')
    (options, args) = parser.parse_args()

    exclude = options.exclude
    include = options.include if options.include else '*'
    file_name = options.file_name

    generate_time_file(include, exclude, file_name)
