from GA import *
import sys
from random import getrandbits
from timeit import timeit

VFUNC = None
# FUTURE Convert to a bitstring only testing script
# This will help measure incremental performance improvements of underlying functions if necessary later.


def numpy_func(arr):
    for i in range(0, len(arr)):
        bs = bitstring.BitArray(auto=arr[i])
        bs.invert()
        arr[i] = bs


def numpy_vfunc(x):
    return not x


def py_func(arr):
    for x in arr:
        x.invert()


def generate_binary(n):
    binary = ''
    for i in range(0, n):
        binary += str(getrandbits(1))
    return binary


class TestRunner(object):
    def __init__(self):
        self.numpyarray = None
        self.numpyarray2 = None
        self.pyarray = None

    def numpy_func_timer(self):
        return numpy_func(self.numpyarray)

    def numpy_vfunc_timer(self):
        global VFUNC
        return VFUNC(self.numpyarray2)

    def py_func_timer(self):
        return py_func(self.pyarray)

    def run_1kb_10(self):
        numpytemparray = []
        for i in range(0, 10):
            numpytemparray.append(bitstring.BitArray(bin=generate_binary(1000)))
        self.numpyarray = np.asarray(numpytemparray, dtype=bool)
        print('numpy memsize:', sys.getsizeof(self.numpyarray), 'bytes')

        self.pyarray = []
        for i in range(0, 10):
            self.pyarray.append(bitstring.BitArray(bin=generate_binary(1000)))
        print('python memsize:', sys.getsizeof(self.pyarray), 'bytes')

        #print('numpy with for loop:',
        #      timeit(self.numpy_func_timer, number=1), 'seconds')

        self.numpyarray2 = self.numpyarray[:]

        print('numpy with vectorize:',
              timeit(self.numpy_vfunc_timer, number=1), 'seconds')
        print('python with for loop:',
              timeit(self.py_func_timer, number=1), 'seconds')

    def run_1kb_100(self):
        numpytemparray = []
        for i in range(0, 100):
            numpytemparray.append(bitstring.BitArray(bin=generate_binary(1000)))
        self.numpyarray = np.asarray(numpytemparray, dtype=bool)
        print('numpy memsize:', sys.getsizeof(self.numpyarray), 'bytes')

        self.pyarray = []
        for i in range(0, 100):
            self.pyarray.append(bitstring.BitArray(bin=generate_binary(1000)))
        print('python memsize:', sys.getsizeof(self.pyarray), 'bytes')

        #print('numpy with for loop:',
        #      timeit(self.numpy_func_timer, number=1), 'seconds')

        self.numpyarray2 = self.numpyarray[:]

        print('numpy with vectorize:',
              timeit(self.numpy_vfunc_timer, number=1), 'seconds')
        print('python with for loop:',
              timeit(self.py_func_timer, number=1), 'seconds')

    def run_1kb_1000(self):
        numpytemparray = []
        for i in range(0, 1000):
            numpytemparray.append(bitstring.BitArray(bin=generate_binary(1000)))
        self.numpyarray = np.asarray(numpytemparray, dtype=bool)
        print('numpy memsize:', sys.getsizeof(self.numpyarray), 'bytes')

        self.pyarray = []
        for i in range(0, 1000):
            self.pyarray.append(bitstring.BitArray(bin=generate_binary(1000)))
        print('python memsize:', sys.getsizeof(self.pyarray), 'bytes')

        #print('numpy with for loop:',
        #      timeit(self.numpy_func_timer, number=1), 'seconds')

        self.numpyarray2 = self.numpyarray[:]

        print('numpy with vectorize:',
              timeit(self.numpy_vfunc_timer, number=1), 'seconds')
        print('python with for loop:',
              timeit(self.py_func_timer, number=1), 'seconds')

    def run_1mb_10(self):
        numpytemparray = []
        for i in range(0, 10):
            numpytemparray.append(bitstring.BitArray(bin=generate_binary(1000000)))
        self.numpyarray = np.asarray(numpytemparray, dtype=bool)
        print('numpy memsize:', sys.getsizeof(self.numpyarray), 'bytes')

        self.pyarray = []
        for i in range(0, 10):
            self.pyarray.append(bitstring.BitArray(bin=generate_binary(1000000)))
        print('python memsize:', sys.getsizeof(self.pyarray), 'bytes')

        #print('numpy with for loop:',
        #      timeit(self.numpy_func_timer, number=1), 'seconds')

        self.numpyarray2 = self.numpyarray[:]

        print('numpy with vectorize:',
              timeit(self.numpy_vfunc_timer, number=1), 'seconds')
        print('python with for loop:',
              timeit(self.py_func_timer, number=1), 'seconds')

    def run_1mb_100(self):
        numpytemparray = []
        for i in range(0, 100):
            numpytemparray.append(bitstring.BitArray(bin=generate_binary(1000000)))
        self.numpyarray = np.asarray(numpytemparray, dtype=bool)
        print('numpy memsize:', sys.getsizeof(self.numpyarray), 'bytes')

        self.pyarray = []
        for i in range(0, 100):
            self.pyarray.append(bitstring.BitArray(bin=generate_binary(1000000)))
        print('python memsize:', sys.getsizeof(self.pyarray), 'bytes')

        #print('numpy with for loop:',
        #      timeit(self.numpy_func_timer, number=1), 'seconds')

        self.numpyarray2 = self.numpyarray[:]

        print('numpy with vectorize:',
              timeit(self.numpy_vfunc_timer, number=1), 'seconds')
        print('python with for loop:',
              timeit(self.py_func_timer, number=1), 'seconds')

    def run_1mb_1000(self):
        numpytemparray = []
        for i in range(0, 1000):
            numpytemparray.append(bitstring.BitArray(bin=generate_binary(1000000)))
        self.numpyarray = np.asarray(numpytemparray, dtype=bool)
        print('numpy memsize:', sys.getsizeof(self.numpyarray), 'bytes')

        self.pyarray = []
        for i in range(0, 1000):
            self.pyarray.append(bitstring.BitArray(bin=generate_binary(1000000)))
        print('python memsize:', sys.getsizeof(self.pyarray), 'bytes')

        #print('numpy with for loop:',
        #     timeit(self.numpy_func_timer, number=1), 'seconds')

        self.numpyarray2 = self.numpyarray[:]

        print('numpy with vectorize:',
              timeit(self.numpy_vfunc_timer, number=1), 'seconds')
        print('python with for loop:',
              timeit(self.py_func_timer, number=1), 'seconds')


if __name__ == '__main__':
    VFUNC = np.vectorize(numpy_vfunc)
    tr = TestRunner()
    print('=========================')
    print('1kb, 10')
    print('=========================')
    tr.run_1kb_10()
    print('=========================')
    print('1kb, 100')
    print('=========================')
    tr.run_1kb_100()
    print('=========================')
    print('1kb, 1000')
    print('=========================')
    tr.run_1kb_1000()
    print('=========================')
    print('1mb, 10')
    print('=========================')
    tr.run_1mb_10()
    print('=========================')
    print('1mb, 100')
    print('=========================')
    tr.run_1mb_100()
    print('=========================')
    print('1mb, 1000')
    print('=========================')
    tr.run_1mb_1000()
# ISSUE Is there a way to support a collection of bitstring.BitArray's that's not a Python list?
# I'm really hesitant to use lists--their implementation is very inefficient for a usecase like this.
# Try rerunning both speed and memory calculations on a more realistic trial set to see, but I'm worried
# the list is just going to explode in size.
