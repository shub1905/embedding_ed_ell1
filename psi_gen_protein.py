# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 14:13:31 2015

@author: patanjali

Refactored to make this more like a sketch. It first initializes parameter
 and randomness. Then iteratively creates a sketch of each string.

#TODO : Move all configuration parameters to one location like delta,...

differ from psi_gen_refactored, reads proteins, alphabet size = 2

"""
from __future__ import division
import shifts_gen
# import data_generation
import protein_read
from collections import defaultdict
import math
import randomness
import pickle
import numpy
import editdistance
import sys

if len(sys.argv) < 3:
  print '''usage: python file.py delta file_suffix'''
  sys.exit(0)

# data_size = int(sys.argv[1])
# data_dim = int(sys.argv[2])
delta = float(sys.argv[1])
file_number = sys.argv[2]
alphabet_size = 26

block_s_metric = defaultdict()
# Data = data_generation.data(data_size, data_dim)
Data = protein_read.read_file_protein()
data_size = len(Data)
data_dim = len(Data[0])

random_s_block = defaultdict()
final_metric = defaultdict()
# delta = data_generation.delta

partitions = shifts_gen.partition_string(Data[0])
num_partitions = len(partitions)


def s_vals():
  x_block = shifts_gen.partition_string(Data[0])[0]
  s_val = []
  s_def = math.log(data_dim * alphabet_size/2, 2)
  j = 0
  while(True):
    s = int(math.ceil(s_def ** j))
    j = j + 1
    if s > len(x_block):
      break
    s_val.append(s)
  return s_val

possible_s = s_vals()

f = lambda x: int(13.5 * x * math.log(x * 1.0 / delta, 2))
R_vals = map(f, possible_s)
print delta
print R_vals

def get_shifts_block(x):
    partitions = shifts_gen.partition_string(x)
    return [[shifts_gen.shifts(x_block, s) for s in possible_s] for x_block in partitions]


def all_random_numbers():
  
  return [[randomness.gen_random(s, len(partitions[j]) - s + 1, R_vals[i]) 
              for i, s in enumerate(possible_s)]
                  for j in xrange(len(partitions))]

random_s_block = all_random_numbers()
      
def final_4d_metric(blocks_shifts_x):
  count = 0
  start = 0
  #embedding = numpy.zeros() #TODO : Preallocate memory for the embedding
  embedding_size = 4*len(blocks_shifts_x)*sum([R_vals[i]*possible_s[i] 
                                          for i in xrange(len(possible_s))])
  embedding = numpy.zeros((embedding_size))
  for block_id in xrange(len(blocks_shifts_x)):
      for s_id in xrange(len(blocks_shifts_x[block_id])):
          count += 1
          #print count
          s = possible_s[s_id]
          I_arr = random_s_block[block_id][s_id]
          r = len(I_arr)
          for u in xrange(r):
              '''
              psi_u_all_v = []
              STR = []
              for j in xrange(s):
                  for ri in I_arr[u]:
                      try:
                          STR.append(blocks_shifts_x[block_id][s_id][j][ri])
                          psi_u_all_v.append(''.join(STR))
                      except:
                          print j, ri
                          raise
              '''
              psi_u_all_v = numpy.bincount([
                      randomness.custom_hash(s, u, ''.join([blocks_shifts_x[block_id][s_id][j][ri] 
                                              for ri in I_arr[u]])) 
                                                  for j in xrange(s)])[1:] * 1.0 / (2 * r)
              embedding[start:(start+psi_u_all_v.shape[0])] = psi_u_all_v
              start += 4*s
              '''
              if count == 1:
                  embedding = numpy.zeros((4*s))
                  embedding[:psi_u_all_v.shape[0]] = psi_u_all_v
              else:
                  temp = numpy.zeros((4*s))
                  temp[:psi_u_all_v.shape[0]] = psi_u_all_v
                  embedding = numpy.concatenate((embedding, temp))
              '''
  return embedding

'''    
def psi(x, r, s, I, u, v):
  
  return sum([v == randomness.custom_hash(s, u, ''.join([x[j][ri] for ri in I])) 
              for j in xrange(s)]) * 1.0 / 2 * r
'''
all_random_numbers()
print 'random numbers generated'

def return_embeddings():
    for i, x in enumerate(Data):
        blocks_shifts_x = get_shifts_block(x)
        if i == 0:
            embedding = final_4d_metric(blocks_shifts_x)
            embeddings = numpy.zeros((len(Data),embedding.shape[0]))
            embeddings[i,:] = embedding
        else:
            embeddings[i,:] = final_4d_metric(blocks_shifts_x)
    return embeddings


if __name__ == '__main__':
    import time
    distortion = 2**(math.sqrt(math.log(data_dim,2)*math.log(math.log(data_dim,2))))

    start_time = time.time()
    for i, x in enumerate(Data):
        #print i
        blocks_shifts_x = get_shifts_block(x)
        if i == 0:
            embedding = final_4d_metric(blocks_shifts_x)
            embeddings = numpy.zeros((len(Data),embedding.shape[0]))
            embeddings[i,:] = embedding
        else:
            embeddings[i,:] = final_4d_metric(blocks_shifts_x)

    embedding_time = time.time() - start_time
    print 'embedding time = ', embedding_time
        
    errors = 0
    distances = numpy.zeros((len(embeddings),len(embeddings),2))
    start_time = time.time()
    for i in xrange(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            l1 = numpy.absolute(embeddings[i]-embeddings[j]).sum()
            distances[i,j,1] = l1

    l1_distance_time = time.time() - start_time
    print 'l1_distance_time time = ', l1_distance_time

    start_time = time.time()
    for i in xrange(len(embeddings)):
      for j in xrange(i+1, len(embeddings)):
          edit = editdistance.eval(Data[i],Data[j])
          distances[i,j,0] = edit

    edit_distance_time = time.time() - start_time
    print 'edit_distance_time = ', edit_distance_time
    time_dict = {
        'embedding_time': embedding_time, 
        'l1_distance_time':l1_distance_time,
        'edit_distance_time':edit_distance_time,
        'total_time':l1_distance_time+embedding_time}

    file_name = 'distances/distances_time_{}_{}_{}_{}.data'.format(data_size, data_dim, delta, file_number)
    numpy.savez(file_name, distances, time_dict)
    '''
    start_time = time.time()    
    for i in xrange(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            edit = editdistance.eval(Data[i],Data[j])
    print time.time() - start_time
    '''