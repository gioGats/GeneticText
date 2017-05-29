from GA import *
import sys
from timeit import timeit


def numpy_func():
    numpyarray = np.array(
        [[bitstring.BitArray(bin='0000'), bitstring.BitArray(bin='1111'), bitstring.BitArray(bin='1001'),
          bitstring.BitArray(bin='0110')],
         [bitstring.BitArray(bin='0001'), bitstring.BitArray(bin='0011'), bitstring.BitArray(bin='0111'),
          bitstring.BitArray(bin='1110')]], dtype=object)
    for x in numpyarray:
        x = x

def numpy_vfunc():
    numpyarray = np.array(
        [[bitstring.BitArray(bin='0000'), bitstring.BitArray(bin='1111'), bitstring.BitArray(bin='1001'),
          bitstring.BitArray(bin='0110')],
         [bitstring.BitArray(bin='0001'), bitstring.BitArray(bin='0011'), bitstring.BitArray(bin='0111'),
          bitstring.BitArray(bin='1110')]], dtype=object)

    def func(x):
        return x

    vfunc = np.vectorize(func)
    vfunc(numpyarray)

def py_func():
    pyarray = [[bitstring.BitArray(bin='0000'), bitstring.BitArray(bin='1111'), bitstring.BitArray(bin='1001'),
                bitstring.BitArray(bin='0110')],
               [bitstring.BitArray(bin='0001'), bitstring.BitArray(bin='0011'), bitstring.BitArray(bin='0111'),
                bitstring.BitArray(bin='1110')]]
    for x in pyarray:
        x = x


numpyarray = np.array(
    [[bitstring.BitArray(bin='0000'), bitstring.BitArray(bin='1111'), bitstring.BitArray(bin='1001'),
      bitstring.BitArray(bin='0110')],
     [bitstring.BitArray(bin='0001'), bitstring.BitArray(bin='0011'), bitstring.BitArray(bin='0111'),
      bitstring.BitArray(bin='1110')]], dtype=bool)
print('numpy memsize:', sys.getsizeof(numpyarray), 'bytes')

pyarray = [[bitstring.BitArray(bin='0000'), bitstring.BitArray(bin='1111'), bitstring.BitArray(bin='1001'),
            bitstring.BitArray(bin='0110')],
           [bitstring.BitArray(bin='0001'), bitstring.BitArray(bin='0011'), bitstring.BitArray(bin='0111'),
            bitstring.BitArray(bin='1110')]]
print('python memsize:', sys.getsizeof(pyarray), 'bytes')

print('numpy with for loop:', timeit('numpy_func()', 'from __main__ import numpy_func', number=10000), 'seconds')
print('numpy with vectorize:', timeit('numpy_vfunc()', 'from __main__ import numpy_vfunc', number=10000), 'seconds')
print('python with for loop:', timeit('py_func()', 'from __main__ import py_func', number=10000), 'seconds')

# What this script does is basically loop through an entire numpy array and a python list of bitstrings 10,000 times.
#
# After trying this out, I am comfortable dropping numpy for bitstring with purpose of speed and efficiency.
# Numpy arrays took up more space in memory, and also were not even compatible, whereas regular lists were
# faster and took less memory space.
# I included a vectorize trial because I know that's one of the things you weren't too keen on giving up, and the
# result shocked me, to say the least.
# If these tests don't make sense or you'd like to try some other tests, by all means go ahead and defintely send me
# the results! Otherwise, if you're okay with it I would just ditch numpy.
#
# When I ran this on my laptop, I got the following scores:
#
# numpy memsize: 160 bytes
# python memsize: 80 bytes
# numpy with for loop: 2.4697435524928055 seconds
# numpy with vectorize: 2.721525941477626 seconds
# python with for loop: 0.9436455130766124 seconds
#
# If you're curious, run the script on your rig and tell me what you get!