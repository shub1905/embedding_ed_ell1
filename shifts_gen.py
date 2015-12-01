import math
import random
NUMBER_BLOCKS = 0


def partition_string(x):
  d = len(x)
  global NUMBER_BLOCKS
  NUMBER_BLOCKS = 2**(math.sqrt(math.log2(d) * math.log(math.log2(d))))
  size_b = int(math.ceil(d / NUMBER_BLOCKS))
  partitions = []
  for i in range(0, d, size_b):
    partitions.append(x[i:i + size_b])
  return partitions


def shifts(string, s):
  shift_partition = []
  N = len(string)
  for i in range(s):
    shift_partition.append(string[i:N - s + i + 1])
  return shift_partition


def main():
  test = ['shifts']
  Dim = 1024
  x = bin(random.getrandbits(Dim))[2:]
  if 'partition_string' in test:
    f = lambda x: (len(x), x)
    partitions = partition_string(x)
    print x[:37]
    print x[37:74]
    print x[-24:], partitions[-1] == x[-24:]
    print map(f, partitions)
    print len(partitions), NUMBER_BLOCKS

  if 'shifts' in test:
    s = math.log2(Dim)
    s = int(math.ceil(s**1))
    shifts_str = shifts(x, s)
    print len(shifts_str) == s


if __name__ == '__main__':
  # Testing for basic output
  main()
