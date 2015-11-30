import math
import random
NUMBER_BLOCKS = 0


def partition_string(x):
  d = len(x)
  global NUMBER_BLOCKS
  NUMBER_BLOCKS = 2**(math.sqrt(math.log(d, 2) * math.log(math.log(d, 2))))
  size_b = int(math.ceil(d / NUMBER_BLOCKS))
  partitions = []
  for i in range(0, d, size_b):
    partitions.append(x[i:i + size_b])

  return partitions


def main():
  Dim = 1024
  x = bin(random.getrandbits(Dim))[2:]
  f = lambda x: (len(x), x)
  partitions = partition_string(x)
  print x[:37]
  print x[37:74]
  print x[-24:], partitions[-1] == x[-24:]
  print map(f, partitions)
  print len(partitions), NUMBER_BLOCKS


if __name__ == '__main__':
  # Testing for basic output
  main()
