import random
import data_generation
import math
import numpy
import xxhash


def gen_random(s, d, r):
  b = int(d * math.log(4 * s) / s)
  choices = numpy.random.choice(range(d), r * b)
  I_arr = []
  for i in range(0, r * b, b):
    I_arr.append(list(choices[i:i + b]))
  return I_arr


def hash(s, u, x):
  has = xxhash.xxh64(x, seed=u).intdigest()
  has = has % (4 * s) + 1
  return has

if __name__ == '__main__':
  gen_random(10, 16, 4, 8)
