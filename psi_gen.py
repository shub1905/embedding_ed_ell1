import shifts_gen
import data_generation
from collections import defaultdict
import math
import randomness

block_s_metric = defaultdict()
Data = data_generation.data()
random_s_block = defaultdict()
final_metric = defaultdict()
R = 10  # to be fixed


def s_vals():
  s_val = []
  s_def = math.log2(data_generation.Dim)
  while(True):
    s = int(math.ceil(s_def ** j))
    j = j + 1
    if s > len(x_block):
      break
    s_val.append(s)
  return s_val


def gen_shifts_block():
  possible_s = s_vals()

  for x_number, x in enumerate(Data):
    partitions = shifts_gen.partition_string(x)
    for x_block_number, x_block in enumerate(partitions):
      for s in possible_s:
        shifts_x_block = shifts_gen.shifts(x_block, s)
        key = '{}_{}_{}'.format(x_number, x_block_number, s)
        block_s_metric[key] = shifts_x_block


def all_random_numbers():
  x = Data[0]
  possible_s = s_vals()
  partitions = shifts_gen.partition_string(x)

  for block_number in range(len(partitions)):
    for s in possible_s:
      key = '{}_{}'.format(block_number, s)
      # TODO discuss dim - s
      I_arr = randomness.gen_random(s, len(x) - s, R)
      H_arr = randomness.hash(s, len(x) - s, R)
      random_s_block[key] = (I_arr, H_arr)


def final_4d_metric():
  for key in block_s_metric:
    [x_ind, x_block_ind, s] = map(int, key.split('_'))
    rand_key = '{}_{}'.format(x_block_ind, s)
    (I_arr, H_arr) = random_s_block[rand_key]

    for u in range(R):
      for v in range(4 * s):
        key_final = '{}_{}_{}'.format(key, u, v)
        final_metric[key_final] = psi(R, s, H_arr[u], I_arr[u], key)


def psi(r, s, H, I, key):
  result = set()
  x_ss = block_s_metric[key]
  for j in range(s):
    x_new = [x_ss[j][ri] for ri in I]
    x_new = ''.join(x_new)
    x_new = int(x_new, 2)
    result.add(H[x_new])

  return len(result)*1.0 / 2*r
