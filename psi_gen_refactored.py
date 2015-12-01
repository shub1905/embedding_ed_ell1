# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 14:13:31 2015

@author: patanjali

Refactored to make this more like a sketch. It first initializes parameter
 and randomness. Then iteratively creates a sketch of each string.

"""

import shifts_gen
import data_generation
from collections import defaultdict
import math
import randomness
#import pudb
import pickle

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

def get_shifts_block(x):
    partitions = shifts_gen.partition_string(x)
    return [[shifts_gen.shifts(x_block, s) for s in possible_s] for x_block in partitions]


def all_random_numbers():
  f = lambda x: int(13.5 * x * math.log(x * 1.0 / delta, 2))
  R_vals = map(f, possible_s)
  return [[randomness.gen_random(s, len(partitions[j]) - s + 1, R_vals[i]) 
              for i, s in enumerate(possible_s)]
                  for j in xrange(len(partitions))]
      
def final_4d_metric():
  count = 0
  for key in block_s_metric:
    print count, key
    count = count + 1
    [x_ind, x_block_ind, s] = map(int, key.split('_'))
    rand_key = '{}_{}'.format(x_block_ind, s)
    I_arr = random_s_block[rand_key]

    R = int(13.5 * s * math.log(s * 1.0 / delta, 2))
    for u in range(R):
      for v in range(4 * s):
        key_final = '{}_{}_{}'.format(key, u, v)
        final_metric[key_final] = psi(R, s, I_arr[u], key, u, v)

def psi(x, r, s, I, u, v):
    
  return sum([v == randomness.custom_hash(s, u, ''.join([x[j][ri] for ri in I])) 
              for j in xrange(s)]) * 1.0 / 2 * r

all_random_numbers()
print 'random numbers generated'

gen_shifts_block()
print 'block shifts calculted', len(block_s_metric)

final_4d_metric()
print 'final metric calculation'
pickle.dump(final_metric, open("final.data", "wb"))
