import random
import data_generation
import math
import numpy


def gen_random(s, d, r):
  b = int(math.ceil(d * math.log(4 * s) / s))
  choices = numpy.random.choice(range(1, d + 1), r * b)
  I_arr = []
  for i in range(0, r * b, b):
    I_arr.append(list(choices[i:i + b]))
  return I_arr


def hash(s, d, r):
  b_ = 2**(int(math.ceil(d * math.log(4 * s) / s)))
  choices = list(numpy.random.choice(range(1, 4 * s + 1), r * b_))
  H_arr = []
  for i in range(0, r * b_, b_):
    H_arr.append(list(choices[i:i + b_]))
  return H_arr

if __name__ == '__main__':
  gen_random(10, 16, 4, 8)
