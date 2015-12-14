# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 17:57:20 2015

@author: patanjali
"""

import numpy
import numpy.linalg
from matplotlib import pyplot

def l_1(x, y, dtype = 'numpy'):
    if dtype == 'list':
        x = numpy.array(x)
        y = numpy.array(y)
        dtype = 'numpy'
    if dtype == 'numpy':
        return numpy.linalg.norm(x-y,1)
    

def l_2(x, y, dtype = 'numpy'):
    if dtype == 'list':
        x = numpy.array(x)
        y = numpy.array(y)
        dtype = 'numpy'
    if dtype == 'numpy':
        return numpy.linalg.norm(x-y,2)
    

def nearest_neighbours_linear_scan(queries, database, distance_function, iterator_type = 'list'):
    
    if queries is database:
        ignore_self = True
        print "Making all vs all comparison"
        
    if iterator_type in ['list', 'numpy']:
        output = numpy.zeros((len(queries), 2))
        for query_index, query in enumerate(queries):
            smallest_distance = float('inf')
            nearest_neighbour = 0
            for index, neighbour in enumerate(database):
                if ignore_self:
                    if query_index == index:
                        continue
                distance = distance_function(query, neighbour)
                if distance < smallest_distance:
                    smallest_distance = distance
                    nearest_neighbour = index
            #print nearest_neighbour, smallest_distance
            output[query_index,0] = nearest_neighbour
            output[query_index,1] = smallest_distance
            
    return output
    
def compare_nearest_neighbours(queries, database, base_metric,
                               base_metric_result, embedded_metric_result,
                               print_summary = True, file_name = 'nn_compare_dist.png'):

    """
    Returns an array with [embedded_nearest_neighbour, embedded_distance, 
                              edit_distance_to_actual_nearest_neighbour,
                              edit_distance_to_embedded_nearest_neighbour
                              ]
    for each of the query points
    """
    
    output = numpy.zeros((embedded_metric_result.shape[0],4))
    output[:, 0:2] = embedded_metric_result
    output[:, 2] = base_metric_result[:,1]
    for query_index, query in enumerate(queries):
        output[query_index, 3] = base_metric(queries[query_index], 
                                            database[int(embedded_metric_result[query_index, 0])])
    if print_summary == True:
        # distance_distribution = (output[:,2]/output[:,3])
        distance_distribution = numpy.zeros(0)
        for i in range(len(output[:,2])):
            if int(output[:,3][i]) != 0:
                distance_distribution = numpy.append(distance_distribution,output[:,2][i]/output[:,3][i])
        distance_distribution.sort()
        print distance_distribution.shape
        
        pyplot.xlabel('Distance to actual neighbour/ Distance of neighbour by approximation')
        pyplot.ylabel('Percentage of observations below Threshold')
        pyplot.plot(distance_distribution, 
                    numpy.arange(distance_distribution.shape[0])*1.0/distance_distribution.shape[0])
        pyplot.savefig(file_name)
    return output