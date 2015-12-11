from __future__ import division
import numpy
import os
import sys


def mean_distortion(file_name):
    dist = numpy.load(file_name)
    dist_p = list(dist['arr_0'])
    distortion = []
    for a in dist_p:
        for b in a:
            if int(b[0]) != 0 and int(b[1] != 0):
                if b[1] > b[0]:
                    print 'ERROR'
                distortion.append(b[0] / b[1])

    print '_'.join(file_name.split('_')[2:]), numpy.mean(distortion), numpy.max(distortion), numpy.min(distortion),
    print numpy.std(distortion), dist['arr_1'].tolist()
    return (numpy.mean(distortion), numpy.std(distortion))


def comp_distortion_variation(delta, file_tuple):
    for file_name in os.listdir('distances/'):
        means = []
        if reduce(lambda x, y: x or y, [x in file_name for x in file_tuple]):
            if file_name.split('_')[4] == delta:
                ans = mean_distortion('distances/' + file_name)
                means.append(ans[0])
    return means


def alphabet_comparison():
    delta = '0.1'
    file_tuple = [['alpha_2.', 'alpha2.'],['alpha26.', 'alpha_26.']]
    for tup in file_tuple:
        means = comp_distortion_variation(delta, tup)
        print '''---------------------------------------'''


def protein_comparison():
    delta = '0.1'
    file_tuple = ['protein']
    means = comp_distortion_variation(delta, file_tuple)

if __name__ == '__main__':
    if 'protein' in sys.argv:
        protein_comparison()
    else:
        alphabet_comparison()
