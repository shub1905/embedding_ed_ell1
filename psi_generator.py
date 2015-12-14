from __future__ import division
from collections import defaultdict
from optparse import OptionParser
import data_generation
import editdistance
import protein_read
import randomness
import shifts_gen
import numpy
import math
import time
import sys


def s_vals():
    x_block = shifts_gen.partition_string(Data[0])[0]
    s_val = []
    s_def = math.log(data_dim * alphabet_size / 2, 2)
    j = 0
    while(True):
        s = int(math.ceil(s_def ** j))
        j = j + 1
        if s > len(x_block):
            break
        s_val.append(s)
    return s_val


def get_shifts_block(x):
    partitions = shifts_gen.partition_string(x)
    return [[shifts_gen.shifts(x_block, s) for s in possible_s] for x_block in partitions]


def all_random_numbers():

    return [[randomness.gen_random(s, len(partitions[j]) - s + 1, R_vals[i])
             for i, s in enumerate(possible_s)]
            for j in xrange(len(partitions))]


def final_4d_metric(blocks_shifts_x):
    count = 0
    start = 0
    embedding_size = 4 * len(blocks_shifts_x) * sum([R_vals[i] * possible_s[i]
                                                     for i in xrange(len(possible_s))])
    embedding = numpy.zeros((embedding_size))
    for block_id in xrange(len(blocks_shifts_x)):
        for s_id in xrange(len(blocks_shifts_x[block_id])):
            count += 1
            s = possible_s[s_id]
            I_arr = random_s_block[block_id][s_id]
            r = len(I_arr)
            for u in xrange(r):
                psi_u_all_v = numpy.bincount([
                    randomness.custom_hash(s, u, ''.join([blocks_shifts_x[block_id][s_id][j][ri]
                                                          for ri in I_arr[u]]))
                    for j in xrange(s)])[1:] * 1.0 / (2 * r)
                embedding[start:(start + psi_u_all_v.shape[0])] = psi_u_all_v
                start += 4 * s

    return embedding


def return_embeddings():
    for i, x in enumerate(Data):
        blocks_shifts_x = get_shifts_block(x)
        if i == 0:
            embedding = final_4d_metric(blocks_shifts_x)
            embeddings = numpy.zeros((len(Data), embedding.shape[0]))
            embeddings[i, :] = embedding
        else:
            embeddings[i, :] = final_4d_metric(blocks_shifts_x)
    return embeddings

def option_parsing():
    parser = OptionParser()
    parser.add_option("-D", "--data", dest="data", default='random', help='type of data = protein, random, typo')
    parser.add_option("-a", "--alphabet", dest="alphabet_size", default=2, help='include files matching all of these regex')
    parser.add_option("-d", "--delta", dest="delta", default='0.1', help='delta, default = 0.1')
    parser.add_option("-n", "--size", dest="size", default='10', help='size of data, default = 10')
    parser.add_option("-m", "--dim", dest="dim", default='10', help='dimention, default = 10')
    parser.add_option("-s", "--suffix", dest="file_suffix", default='', help='distortion file suffix')
    parser.add_option("-t", "--typo", dest="typos", default='5', help='number of typos in string only valid if data=typo, default = 5')
    parser.add_option("-f", "--file", dest="file", default='raw_data/multigene_zfill.txt', help='data source only valid if data=protein, default = raw_data/multigene_zfill.txt')

    (options, args) = parser.parse_args()
    return (options, args)

if __name__ == '__main__':
	[options, _] = option_parsing()
	print options.data