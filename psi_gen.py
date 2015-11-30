import shifts_gen
import data_generation
from collections import defaultdict
import pudb
import math

block_s_metric = defaultdict()
pudb.set_trace()


def main():
  Data = data_generation.data()
  for x_number, x in enumerate(Data):
    partitions = shifts_gen.partition_string(x)
    for x_block_number, x_block in enumerate(partitions):
      j = 0
      s_def = math.log(data_generation.Dim, 2)
      while(True):
        s = int(math.ceil(s_def ** j))
        j = j + 1
        if s > len(x_block):
          break
        shifts_x_block = shifts_gen.shifts(x_block, s)
        key = '{}_{}_{}'.format(x_number, x_block_number, s)
        block_s_metric[key] = shifts_x_block

main()
