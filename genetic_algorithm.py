# TODO Pull GA implementation out of AY17-1/CS3610
# TODO Convert implementation to numpy.array(dtype='uint8')
# TODO Convert implementation to an interface-inheirtance
# FUTURE Bit-level implementation


class GeneticAlgorithm(object):
    def __init__(self, target=None):
        self.target = target

    def step(self, verbose=False):
        if verbose:
            return []
        else:
            return None