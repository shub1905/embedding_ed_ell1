import random
import string
import numpy
from pprint import pprint


def data(N, Dim):
    # Data = ['adfadfdfafgfgafgfgafadfagfafbfbba','adfaduioffgfgafgfgafadqwerafbfbba']
    ''.join(random.choice(string.ascii_lowercase) for _ in range(Dim))
    if N >= 2**Dim:
        Data = [bin(i)[2:].zfill(Dim) for i in xrange(2**Dim)]
    else:
        Data = [bin(random.getrandbits(Dim))[2:].zfill(Dim) for i in xrange(N)]
        # Data = [''.join(random.choice(string.ascii_lowercase) for _ in range(Dim)) for i in xrange(N)]

    return Data


def insertion(srt, indx, alphabet_sample='01'):
    srt_new = srt[:indx] + random.choice(alphabet_sample) + srt[indx:]
    return srt_new


def deletion(srt, indx, alphabet_sample='01'):
    return srt[:indx] + srt[indx + 1:]


def subsitution(srt, indx, alphabet_sample='01'):
    srt_new = srt[:indx] + random.choice(alphabet_sample) + srt[indx + 1:]
    return srt_new


def data_typo(Dim, k=1, typos=100, alphabet_sample='01'):
    '''
    rand {0,1,2 : insertion, deletion, subsitution}
    '''
    Data_seed = bin(random.getrandbits(Dim))[2:].zfill(Dim)
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

    for i,d in enumerate(Data):
        Data[i] = Data[i].ljust(max_len, '*')
    return Data


if __name__ == '__main__':
    # import time
    # for N in [2, 4, 8, 16]:
    #     for Dim in [1024, 2048, 4096, 8192]:
    #         start_time = time.time()
    #         data()
    #         print N, Dim, time.time() - start_time
    pprint(data_typo(10, k=5, typos=10))
