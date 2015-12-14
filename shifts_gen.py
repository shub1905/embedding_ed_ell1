import math
import random
NUMBER_BLOCKS = 0


def partition_string(x):
  d = len(x)
  global NUMBER_BLOCKS
  NUMBER_BLOCKS = int(2**(math.sqrt(math.log(d, 2) * math.log(math.log(d, 2), 2))))
  size_b = int(d * 1.0 / NUMBER_BLOCKS)
  remainder = d % NUMBER_BLOCKS

  end_points = [i*size_b for i in xrange(NUMBER_BLOCKS-remainder+1)]
  end_points += [end_points[-1] + i*(size_b+1) for i in xrange(1,remainder+1)]
  partitions = [x[end_points[i]:end_points[i+1]] for i in xrange(len(end_points)-1)]

  return partitions


def shifts(string, s):
  N = len(string)
  shift_partition  = [string[i:N - s + i + 1] for i in xrange(s)]
  return shift_partition


def main():
  test = ['partition_string','shifts']
  Dim = 1024
  x = bin(random.getrandbits(Dim))[2:]
  x = x.zfill(Dim)
  if 'partition_string' in test:
    f = lambda x: (len(x), x)
    partitions = partition_string(x)
    print map(f, partitions)
    print len(partitions), NUMBER_BLOCKS

  if 'shifts' in test:
    s = math.log(Dim, 2)
    s = int(math.ceil(s**1))
    shifts_str = shifts(x[:101], s)
    print len(shifts_str) == s


if __name__ == '__main__':
  main()
