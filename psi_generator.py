from __future__ import division
from collections import defaultdict
from optparse import OptionParser
import data_generation
import editdistance
import randomness
import shifts_gen
import string
import numpy
import math
import time
import sys


def s_vals(data_0, alphabet_size, data_dim):
    x_block = shifts_gen.partition_string(data_0)[0]
    s_val = []
    s_def = math.log(data_dim * alphabet_size / 2, 2)
    j = 0
    while(True):
        s = int(math.ceil(s_def ** j))
        j = j + 1
        # Modification to original algorithm
        if s > len(x_block) or j > 2:
            break
        s_val.append(s)
    return s_val


def possible_r_vals(delta, possible_s):
    f = lambda x: int(13.5 * x * math.log(x * 1.0 / delta, 2))
    R_vals = map(f, possible_s)
    return R_vals


def get_shifts_block(x, possible_s):
    partitions = shifts_gen.partition_string(x)
    return [[shifts_gen.shifts(x_block, s) for s in possible_s] for x_block in partitions]


def all_random_numbers(possible_s, partitions, R_vals):
    return [[randomness.gen_random(s, len(partitions[j]) - s + 1, R_vals[i])
             for i, s in enumerate(possible_s)]
            for j in xrange(len(partitions))]


def final_4d_metric(blocks_shifts_x, R_vals, possible_s, random_s_block):
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
                psi_u_all_v = numpy.bincount([randomness.custom_hash(s, u, ''.join([blocks_shifts_x[block_id][s_id][
                                             j][ri] for ri in I_arr[u]])) for j in xrange(s)])[1:] * 1.0 / (2 * r)
                embedding[start:(start + psi_u_all_v.shape[0])] = psi_u_all_v
                start += 4 * s

    return embedding


def return_embeddings(Data, random_s_block, R_vals, possible_s):
    start_time = time.time()
    for i, x in enumerate(Data):
        blocks_shifts_x = get_shifts_block(x, possible_s)
        if i == 0:
            embedding = final_4d_metric(blocks_shifts_x, R_vals, possible_s, random_s_block)
            embeddings = numpy.zeros((len(Data), embedding.shape[0]))
            embeddings[i, :] = embedding
        else:
            embeddings[i, :] = final_4d_metric(blocks_shifts_x, R_vals, possible_s, random_s_block)

    embedding_time = time.time() - start_time
    print 'embedding time = ', embedding_time
    return (embeddings, embedding_time)


def return_l1_distance(embeddings, distances):
    start_time = time.time()
    for i in xrange(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            l1 = numpy.absolute(embeddings[i] - embeddings[j]).sum()
            distances[i, j, 1] = l1

    l1_distance_time = time.time() - start_time
    print 'l1_distance_time time = ', l1_distance_time
    return l1_distance_time


def return_edit_distance(Data, embeddings, distances):
    start_time = time.time()
    for i in xrange(len(embeddings)):
        for j in xrange(i + 1, len(embeddings)):
            edit = editdistance.eval(Data[i], Data[j])
            distances[i, j, 0] = edit

    edit_distance_time = time.time() - start_time
    print 'edit_distance_time = ', edit_distance_time
    return edit_distance_time


def driver_function(Data, options):
    data_dim = len(Data[0])
    data_size = len(Data)

    possible_s = s_vals(Data[0], options.alphabet_size, data_dim)
    R_vals = possible_r_vals(options.delta, possible_s)

    partitions = shifts_gen.partition_string(Data[0])
    random_s_block = all_random_numbers(possible_s, partitions, R_vals)

    (embeddings, embed_time) = return_embeddings(Data, random_s_block, R_vals, possible_s)
    distances = numpy.zeros((len(embeddings), len(embeddings), 2))
    l1_time = return_l1_distance(embeddings, distances)
    edit_time = return_edit_distance(Data, embeddings, distances)

    time_dict = {
        'embedding_time': embed_time,
        'l1_distance_time': l1_time,
        'edit_distance_time': edit_time,
        'total_time': l1_time + embed_time}

    file_name = 'distances/distances_time_{}_{}_{}_{}.data'.format(
        data_size, data_dim, options.delta, options.file_suffix)
    numpy.savez(file_name, distances, time_dict)


def option_parsing(print_usage=False):
    parser = OptionParser()
    parser.add_option("-D", "--data", dest="data", default='random',
                      help='type of data = protein, random, typo')
    parser.add_option("-a", "--alphabet", dest="alphabet_size", default=2,
                      type='int', help='include files matching all of these regex')
    parser.add_option("-d", "--delta", dest="delta", default='0.1',
                      type='float', help='delta, default = 0.1')
    parser.add_option("-n", "--size", dest="size", default='10',
                      type='int', help='size of data, default = 10')
    parser.add_option("-m", "--dim", dest="dim", default='10',
                      type='int', help='dimention, default = 10')
    parser.add_option("-s", "--suffix", dest="file_suffix",
                      default='', help='distortion file suffix')
    parser.add_option("-t", "--typo", dest="typos", default='5', type='int',
                      help='number of typos in string only valid if data=typo, default = 5')
    parser.add_option("-f", "--file", dest="file", default='raw_data/multigene_zfill.txt',
                      help='data source only valid if data=protein, default = raw_data/multigene_zfill.txt')

    if print_usage:
        parser.print_help()
        return None
    else:
        (options, args) = parser.parse_args()
        return (options, args)


def print_config(options):
    print options


if __name__ == '__main__':
    [options, _] = option_parsing()
    print_config(options)

    if options.data == 'random':
        Data = data_generation.random_data_generation(
            options.size, options.dim, options.alphabet_size)
    elif options.data == 'typo':
        Data = data_generation.data_typo(options.dim, options.typos, options.alphabet_size)
    elif options.data == 'protein':
        Data = data_generation.read_file_protein(file_name=options.file)
    else:
        option_parsing(print_usage=True)
        sys.exit(0)

    driver_function(Data, options)
