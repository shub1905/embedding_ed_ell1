# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 14:13:31 2015

@author: patanjali

Refactored to make this more like a sketch. It first initializes parameter
 and randomness. Then iteratively creates a sketch of each string.

#TODO : Move all configuration parameters to one location like delta,...

"""

import shifts_gen
import data_generation
from collections import defaultdict
import math
import randomness
#import pudb
import pickle
import numpy
import editdistance

block_s_metric = defaultdict()
Data = data_generation.data()
random_s_block = defaultdict()
final_metric = defaultdict()
delta = 0.1

partitions = shifts_gen.partition_string(Data[0])
num_partitions = len(partitions)

def s_vals():
  x_block = shifts_gen.partition_string(Data[0])[0]
  s_val = []
  s_def = math.log(data_generation.Dim, 2)
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

if __name__ == '__main__':
    import time
    distortion = 2**(math.sqrt(math.log(data_generation.Dim)*math.log(math.log(data_generation.Dim))))
    embeddings = [0 for x in Data]

    start_time = time.time()
    for i, x in enumerate(Data):
        print i
        blocks_shifts_x = get_shifts_block(x)
        embeddings[i] = final_4d_metric(blocks_shifts_x)
    print time.time() - start_time
        
    start_time = time.time()
    for i in xrange(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            l1 = sum(abs(embeddings[i]-embeddings[j]))
#            if max(l1/edit, edit/l1) > distortion:
#                print l1, edit, max(l1/edit, edit/l1), distortion
    print time.time() - start_time
    
    start_time = time.time()    
    for i in xrange(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            edit = editdistance.eval(Data[i],Data[j])
    print time.time() - start_time
'''
print 'block shifts calculted', len(block_s_metric)

final_4d_metric()
print 'final metric calculation'
pickle.dump(final_metric, open("final.data", "wb"))
'''