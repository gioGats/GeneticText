# We have an ISSUE with compatibility between numpy and bitstring

# Here is an example

import numpy as np
import bitstring

# a is a BitArray on the fast, bit-level implementation of bitstring
a = bitstring.BitArray(bin='0000000011111111')
print(a, type(a))

# if we then drop a into a numpy array, it automatically type converts
b = np.array(a)
print(b, type(b), b.dtype, b.shape)

# numpy is fast, but the Data types docs says:

# Data type	    Description
# bool_	        Boolean (True or False) stored as a byte

# Byte-level storage is why we sided with bitstring originally.
# To ensure that the use of numpy arrays within the
# GeneticAlgorithm class don't undo the performance gains of ga_utils,
# I've added unittests to ga.py, which should include some performance testing.
# This isn't entirely additional, though, because good testing should check
# both performance and correctness.

# There is an additional ISSUE with the current implementation

# if we start with an empty array, c, it's default dtype is float64 (8 bytes per float!)
c = np.empty((1, 16))
print(c, type(c), c.dtype, c.shape)
# when we drop a into c, it automatically type converts again.
c[0] = a
print(c, type(c), c.dtype, c.shape)

# if we specfy dtype, it seems to correct this
d = np.empty((1, 16), dtype=np.bool)
print(d, type(d), d.dtype, d.shape)
d[0] = a
print(d, type(d), d.dtype, d.shape)

# We still need to investigate the performance implications here before moving forward.
