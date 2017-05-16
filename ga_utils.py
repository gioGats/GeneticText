import numpy as np
# TODO Decide on a binary library
# (is numpy bool overhead too much?)
# (can we do better?)
from random import randint


def str_to_bin(string):
    """
    Convert string to binary representation
    :param string: str to convert
    :return: binary sequence
    """
    # TODO Implement str_to_bin
    raise NotImplementedError


def create_random(n, bits=True):
    """
    Create a random sequence of length n
    :param n: int
    :param bits: if True each item is a bit; else each item is a character
    :return: binary sequence or str
    """
    # TODO Implement create_random
    raise NotImplementedError


def midpoint_xover(a, b, midpoint):
    """
    Do a midpoint crossover of a and b
    :raises ValueError if len(a) != len(b); ValueError if midpoint is not [0.0, 1.0] or [0, len(a)]
    :param a: binary sequence
    :param b: binary sequence
    :param midpoint: if float, take first midpoint percent of a and last (1-midpoint) percent of b
                     if int, take first midpoint items of a and last (length-midpoint) items of b
    :return: binary sequence
    """
    # TODO Implement midpoint_xover
    raise NotImplementedError


def location_mutation(a, start=0, end=None):
    """
    Flips the bits of a between position start and position end
    :param a: binary sequence
    :param start: int position (or float percentage) to start flipping
    :param end: int position (or float percentage) to stop flipping, set to len(a) if end is None.
    :return: binary sequence
    """
    if isinstance(start, float):
        start = int(min(max(start, 0.0), 1.0) * len(a))
    if isinstance(end, float):
        end = int(min(max(end, 0.0), 1.0) * len(a))
    elif end is None:
        end = len(a)
    assert start < end
    # TODO Implement location_mutation
    raise NotImplementedError


def probability_mutation(a, pflip, start=0, end=None):
    """
    Flips the bits of a between position start and position end with probability pflip
    :param a: binary sequence
    :param pflip: float (0,1); if random.random() > pflip, flip that bit
    :param start: int position (or float percentage) to start flipping
    :param end: int position (or float percentage) to stop flipping, set to len(a) if end is None.
    :return: binary sequence
    """
    if isinstance(start, float):
        start = int(min(max(start, 0.0), 1.0) * len(a))
    if isinstance(end, float):
        end = int(min(max(end, 0.0), 1.0) * len(a))
    elif end is None:
        end = len(a)
    assert start < end
    # TODO Implement probability_mutation
    raise NotImplementedError


def score_sequence(test, answer):
    """
    Scores a binary sequence against a correct sequence
    :raises ValueError if len(test) != len(answer)
    :param test: binary sequence
    :param answer: binary sequence
    :return: float [0,1]; (number of bits in test that match answer)/(number of bits in answer)
    """
    # TODO Implement score
    raise NotImplementedError


def probability_selection(population):
    """
    Selects a value from a population given a probability distribution
    :param population: iterable of tuples, where [1] is value and [0] is probability of selection
        probabilities must all be ints (relative frequency) or floats (likelihood), else raises ValueError
    :return: value of the selected item
    """
    # TODO Implement probability_selection
    raise NotImplementedError


def ranked_selection(population):
    """
    Selects a value from a population prioritized by rank
    :param population: sorted iterable of current population
    :return: value of the selected item
    """
    return population[min(randint(0, len(population)-1), randint(0, len(population)-1))]


if __name__ == '__main__':
    import unittest

    class TestGAUtils(unittest.TestCase):
        def setUp(self):
            pass

        def test_str_to_bin(self):
            # TODO Implement test_str_to_bin
            self.fail('Not implemented')

        def test_create_random(self):
            # TODO Implement test_create_random
            self.fail('Not implemented')

        def test_midpoint_xover(self):
            # TODO Implement test_midpoint_xover
            self.fail('Not implemented')

        def test_location_mutation(self):
            # TODO Implement test_location_mutation
            self.fail('Not implemented')

        def test_probability_mutation(self):
            # TODO Implement test_probability_mutation
            self.fail('Not implemented')

        def test_score_sequence(self):
            # TODO Implement test_score_sequence
            self.fail('Not implemented')

        def test_probability_selection(self):
            # TODO Implement test_probability_selection
            self.fail('Not implemented')

        def test_ranked_selection(self):
            # TODO Implement test_ranked_selection
            self.fail('Not implemented')

        def tearDown(self):
            pass

    unittest.main(verbosity=2)
