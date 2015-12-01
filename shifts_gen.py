import math
import random
NUMBER_BLOCKS = 0


def partition_string(x):
  d = len(x)
  global NUMBER_BLOCKS
  NUMBER_BLOCKS = int(2**(math.sqrt(math.log(d, 2) * math.log(math.log(d, 2), 2))))
  size_b = int(d * 1.0 / NUMBER_BLOCKS)
  reminder = d % NUMBER_BLOCKS
  partitions = []

  s = 0
  while(True):
    if (s >= d):
      break
    t = s + size_b
    if reminder > 0:
      reminder = reminder - 1
      t = t + 1

    partitions.append(x[s:t])
    s = t
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
    print s, shifts_str
    print len(shifts_str) == s


if __name__ == '__main__':
  main()
