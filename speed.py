from GA import *
import sys
from timeit import timeit

# ISSUE Test on realistic size examples.
# These are all four bits; target_data/films/argo.txt is 138914 characters and 1126304 bits long.
# If we measure out to 2 decimal places (we actually measure closer to 12),
# even if there is a 200% difference in timing between 0.002 and 0.001, we will
# measure them as 0.00.  Use longer and more complex tasks to better test performance.


def numpy_func():
    numpyarray = np.array(
        [[bitstring.BitArray(bin='0000'), bitstring.BitArray(bin='1111'), bitstring.BitArray(bin='1001'),
          bitstring.BitArray(bin='0110')],
         [bitstring.BitArray(bin='0001'), bitstring.BitArray(bin='0011'), bitstring.BitArray(bin='0111'),
          bitstring.BitArray(bin='1110')]], dtype=object)
    # ISSUE These are dtype=object, when really the closest approximation would be dtype=bool.
    # Try both, it might make a difference.

    for x in numpyarray:
        # ISSUE Do an actual operation, like flip all bits
        # If the function runtime is effectively zero, the system will run at the speed of memory access;
        # In such a setting, parallelization or vectorization won't help much.  But in practice, our functions
        # will have a non-zero runtime.  So we should test on a non-zero setting.
        x = x

def numpy_vfunc():
    numpyarray = np.array(
        [[bitstring.BitArray(bin='0000'), bitstring.BitArray(bin='1111'), bitstring.BitArray(bin='1001'),
          bitstring.BitArray(bin='0110')],
         [bitstring.BitArray(bin='0001'), bitstring.BitArray(bin='0011'), bitstring.BitArray(bin='0111'),
          bitstring.BitArray(bin='1110')]], dtype=object)

    def func(x):
        return x

    # ISSUE These results don't make sense.
    # Vectorized functions should be faster than for-loop functions.
    # This could be from using just an identity function, but also could
    # be because there's fairly substantial overhead coming from np.vectorize.
    # To counteract this, don't redefine and vectorize "func" every iteration,
    # do it once and then use that vectorized function repeatidly.
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
# ISSUE Is there a way to support a collection of bitstring.BitArray's that's not a Python list?
# I'm really hesitant to use lists--their implementation is very inefficient for a usecase like this.
# Try rerunning both speed and memory calculations on a more realistic trial set to see, but I'm worried
# the list is just going to explode in size.
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