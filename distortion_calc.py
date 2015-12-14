from __future__ import division
import numpy
import os
import sys
import common
from optparse import OptionParser


def mean_distortion(file_name):
    dist = numpy.load(file_name)
    dist_p = list(dist['arr_0'])
    distortion = []
    for a in dist_p:
        for b in a:
            if int(b[0]) != 0 and int(b[1] != 0):
                temp = max(b[0] / b[1], b[1] / b[0])
                distortion.append(temp)

    print '_'.join(file_name.split('_')[2:]), numpy.mean(distortion), numpy.max(distortion), numpy.min(distortion),
    print numpy.std(distortion), dist['arr_1'].tolist()
    return (numpy.mean(distortion), numpy.std(distortion))


def comp_distortion_variation(include, exclude, delta='0.1'):
    files = common.get_file_names(include, exclude)
    for file_name in files:
        means = []
        ans = mean_distortion('distances/' + file_name)
        means.append(ans[0])
    return means

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-e", "--exclude", dest="exclude", action='append',
                      help='exclude all files matching these regex')
    parser.add_option("-i", "--include", dest="include", action='append',
                      help='include files matching all of these regex')
    (options, args) = parser.parse_args()

    exclude = options.exclude
    include = options.include if options.include else '*'
    print include, exclude
    comp_distortion_variation(include, exclude)
