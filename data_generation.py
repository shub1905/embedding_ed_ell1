import random
import string
import numpy


def data(N, Dim):
    # Data = ['adfadfdfafgfgafgfgafadfagfafbfbba','adfaduioffgfgafgfgafadqwerafbfbba']
    ''.join(random.choice(string.ascii_lowercase) for _ in range(Dim))
    if N >= 2**Dim:
        Data = [bin(i)[2:].zfill(Dim) for i in xrange(2**Dim)]
    else:
        Data = [bin(random.getrandbits(Dim))[2:].zfill(Dim) for i in xrange(N)]
        # Data = [''.join(random.choice(string.ascii_lowercase) for _ in range(Dim)) for i in xrange(N)]

    return Data


def data_typo(Dim, k=1, typos=100):
    '''
    rand {0,1,2 : insertion, deletion, subsitution}
    '''
    Data = [bin(random.getrandbits(Dim))[2:].zfill(Dim)]
    sample = numpy.random.choice(range(Dim), k*typo)
    for t in range(typos):


if __name__ == '__main__':
    import time
    for N in [2, 4, 8, 16]:
        for Dim in [1024, 2048, 4096, 8192]:
            start_time = time.time()
            data()
            print N, Dim, time.time() - start_time
