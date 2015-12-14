import random
import string
import numpy
import sys
import time


def random_data_generation(N, Dim, alphabet_size=2):
    if N >= 2**Dim and alphabet_size == 2:
        Data = [bin(i)[2:].zfill(Dim) for i in xrange(2**Dim)]
    else:
        if alphabet_size == 2:
            Data = [bin(random.getrandbits(Dim))[2:].zfill(Dim) for i in xrange(N)]
        else:
            sample = string.ascii_lowercase[:alphabet_size]
            Data = [''.join(random.choice(sample) for _ in range(Dim)) for i in xrange(N)]

    return Data


def insertion(srt, indx, alphabet_sample='01'):
    srt_new = srt[:indx] + random.choice(alphabet_sample) + srt[indx:]
    return srt_new


def deletion(srt, indx, alphabet_sample='01'):
    return srt[:indx] + srt[indx + 1:]


def subsitution(srt, indx, alphabet_sample='01'):
    srt_new = srt[:indx] + random.choice(alphabet_sample) + srt[indx + 1:]
    return srt_new


def data_typo(Dim, k=1, typos=100, alphabet_size=2):
    '''
    rand {0,1,2 : insertion, deletion, subsitution}
    '''
    if alphabet_size == 2:
        alphabet_sample = '01'
        Data_seed = bin(random.getrandbits(Dim))[2:].zfill(Dim)
    else:
        alphabet_sample = string.ascii_lowercase[:alphabet_size]
        Data_seed = ''.join(numpy.random.choice(list(alphabet_sample), Dim))

    sample = numpy.random.choice(range(Dim), k * typos)
    Data = []
    function_hash = {0: insertion, 1: deletion, 2: subsitution}
    max_len = 0

    for t in range(typos):
        temp_mod = Data_seed
        for i in range(k):
            string_index = sample[t * k + i]
            temp_mod = function_hash[random.randint(0, 2)](temp_mod, string_index, alphabet_sample)
        max_len = max(max_len, len(temp_mod))
        Data.append(temp_mod)

    Data.append(Data_seed)

    for i, d in enumerate(Data):
        Data[i] = Data[i].ljust(max_len, '*')
    return Data


def read_file_protein(file_name=None):
    if file_name == None:
        file_name = 'raw_data/UniProt.txt'

    file_handle = open(file_name, 'r')
    header_line = file_handle.readline()
    proteins = []
    for line in file_handle:
        line = line.replace('\n', '')
        proteins.append(line.split('\t')[-1])

    file_handle.close()
    return proteins


if __name__ == '__main__':
    # Testing random data generation
    for N in [2, 4, 8, 16]:
        for Dim in [1024, 2048, 4096, 8192]:
            start_time = time.time()
            random_data_generation(N, Dim, 2)
            random_data_generation(N, Dim, 26)
            print N, Dim, time.time() - start_time

    # Testing typo data generation
    print data_typo(10, k=5, typos=10, alphabet_size=20)

    # Testing protein read
    file_name = None
    if len(sys.argv) < 2:
        file_name = 'raw_data/UniProt.txt'
    else:
        file_name = sys.argv[1]
    proteins = read_file_protein(None)
    print len(proteins)
