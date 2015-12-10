from __future__ import division
import numpy
import os

def mean_distortion(file_name):
    distortion = []
    dist = numpy.load(file_name)
    dist_p = list(dist['arr_0'])
    for a in dist_p:
        for b in a:
            if int(b[0]) != 0 and int(b[1]!=0):
                distortion.append(b[0]/b[1])

    print file_name.split('_')[2:5], numpy.mean(distortion), numpy.std(distortion), dist['arr_1'].tolist()['total_time']
    return (numpy.mean(distortion), numpy.std(distortion))
    

delta = '0.9'
for file_name in os.listdir('distances/'):
    means = []
    if 'alpha_2.' in file_name or 'alpha2.' in file_name:
        if file_name.split('_')[4] == delta:
#         print file_name
            ans = mean_distortion('distances/'+file_name)
            means.append(ans[0])
print '''-----------------26----------------------'''
for file_name in os.listdir('distances/'):
    means = []
    if 'alpha_26.' in file_name or 'alpha26.' in file_name:
        if file_name.split('_')[4] == delta:
#         print file_name
            ans = mean_distortion('distances/'+file_name)
            means.append(ans[0])