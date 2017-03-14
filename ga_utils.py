import numpy as np
# TODO Decide on a binary library
# (is numpy bool overhead too much?)
# (can we do better?)


def str_to_bin(string):
    """
    Convert string to binary representation
    :param string: str to convert
    :return: binary sequence
    """
    raise NotImplementedError


def create_random(n, bits=True):
    """
    Create a random sequence of length n
    :param n: int
    :param bits: if True each item is a bit; else each item is a character
    :return: binary sequence or str
    """
    raise NotImplementedError


def midpoint_xover(a, b, midpoint):
    """
    Do a midpoint crossover of a and b
    :raises ValueError if len(a) != len(b)
    :param a: binary sequence
    :param b: binary sequence
    :param midpoint: if float, take first midpoint percent of a and last (1-midpoint) percent of b
                     if int, take first midpoint items of a and last (length-midpoint) items of b
    :return: binary sequence
    """
    raise NotImplementedError


def location_mutation(a, start=0, end=None):
    """
    Flips the bits of a between position start and position end
    :param a: binary sequence
    :param start: int position to start flipping
    :param end: int position to stop flipping, set to len(a) if end is None.
    :return: binary sequence
    """
    raise NotImplementedError


def probability_mutation(a, pflip, start=0, end=None):
    """
    Flips the bits of a between position start and position end with probability pflip
    :param a: binary sequence
    :param pflip: float (0,1); if random.random() > pflip, flip that bit
    :param start: int position to start flipping
    :param end: int position to stop flipping, set to len(a) if end is None.
    :return: binary sequence
    """
    raise NotImplementedError


def score(test, answer):
    """
    Scores a binary sequence against a correct sequence
    :raises ValueError if len(test) != len(answer)
    :param test: binary sequence
    :param answer: binary sequence
    :return: float [0,1]; (number of bits in test that match answer)/(number of bits in answer)
    """
    raise NotImplementedError

if __name__ == '__main__':
    import unittest

    class TestGAUtils(unittest.TestCase):
        def setUp(self):
            pass

        def test_str_to_bin(self):
            self.fail('Not implemented')

        def test_(self):
            self.fail('Not implemented')

        def test_create_random(self):
            self.fail('Not implemented')

        def test_midpoint_xover(self):
            self.fail('Not implemented')

        def test_location_mutation(self):
            self.fail('Not implemented')

        def test_probability_mutation(self):
            self.fail('Not implemented')

        def test_score(self):
            self.fail('Not implemented')

        def tearDown(self):
            pass

    unittest.main(verbosity=2)
