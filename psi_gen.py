import shifts_gen
import data_generation
from collections import defaultdict
import math
import randomness
import pudb
import pickle

block_s_metric = defaultdict()
Data = data_generation.data()
random_s_block = defaultdict()
final_metric = defaultdict()
delta = 0.1


def s_vals():
  x_block = shifts_gen.partition_string(Data[0])[0]
  s_val = []
  s_def = math.log(data_generation.Dim, 2)
  j = 0
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
  f = lambda x: int(13.5 * x * math.log(x * 1.0 / delta, 2))
  R_vals = map(f, possible_s)
  partitions = shifts_gen.partition_string(x)

  for block_number in range(len(partitions)):
    for i, s in enumerate(possible_s):
      key = '{}_{}'.format(block_number, s)
      I_arr = randomness.gen_random(s, len(partitions[block_number]) - s + 1, R_vals[i])
      random_s_block[key] = I_arr


def final_4d_metric():
  for key in block_s_metric:
    [x_ind, x_block_ind, s] = map(int, key.split('_'))
    rand_key = '{}_{}'.format(x_block_ind, s)
    I_arr = random_s_block[rand_key]

    R = int(13.5 * s * math.log(s * 1.0 / delta, 2))
    for u in range(R):
      for v in range(4 * s):
        key_final = '{}_{}_{}'.format(key, u, v)
        final_metric[key_final] = psi(R, s, I_arr[u], key, u, v)


def psi(r, s, I, key, u, v):
  result = []
  x_ss = block_s_metric[key]
  for j in range(s):
    x_new = [x_ss[j][ri] for ri in I]
    x_new = ''.join(x_new)
    x_new = int(x_new, 2)
    result.append(v == randomness.hash(s, u, x_new))

  return sum(result) * 1.0 / 2 * r

all_random_numbers()
gen_shifts_block()
final_4d_metric()
pickle.dump(final_metric, open("final.data", "wb"))
