import random
import data_generation
import math
import numpy
import xxhash


def gen_random(s, d, r):
  b = int(d * math.log(4 * s) / s)
  choices = numpy.random.choice(d, r * b)
  I_arr = [list(choices[i*b:(i+1)*b]) for i in xrange(r)]
  return I_arr

def custom_hash(s, u, x):
  has = xxhash.xxh64(x, seed=u).intdigest()
  has = has % (4 * s) + 1
  return has

if __name__ == '__main__':
  gen_random(10, 16, 4)
