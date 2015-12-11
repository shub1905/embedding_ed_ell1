import os
import math
import sys


def calculate(size, dim, delta, number):
    function_str = 'python psi_gen_refactored.py {} {} {} {}'.format(size, dim, delta, number)
    os.system(function_str)

if __name__ == '__main__':
    number = sys.argv[1]
    dimensions = [2**x for x in range(10, 15)]
    # size = [int(math.ceil(1024 * 20 / x * scale)) for x in dimensions]
    delta = [0.01, 0.05, 0.1, 0.5, 0.9]

    for i in range(len(dimensions)):
        for j in range(len(delta)):
            size = 1024 * 20 / dimensions[i]
            size = max(int(math.ceil(size)), 2)
            print 'run count = ', size, dimensions[i], delta[j]
            calculate(size, dimensions[i], delta[j], number)
