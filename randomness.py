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

  print I_arr


def hash(s, r):
  return list(numpy.random.choice(range(1, 4 * s + 1), r))

if __name__ == '__main__':
  gen_random(10, 16, 4, 8)
