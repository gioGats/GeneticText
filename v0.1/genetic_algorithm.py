import numpy as np
import random
# TODO Convert implementation to numpy.array(dtype='uint8')
# TODO Convert implementation to an interface-inheirtance
# FUTURE Replace numpy with a bit level implemenation


class GeneticAlgorithm(object):
    def __init__(self, target=None):
        self.target = target

    def step(self, verbose=False):
        if verbose:
            return []
        else:
            return None
