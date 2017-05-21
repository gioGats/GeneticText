import random

import numpy as np
import bitstring
from random import randint


def str_to_bin(string):
    """
    Convert string to binary representation
    :param string: str to convert
    :return: binary sequence
    """
    string_bytes = str.encode(string)
    string_bits = bitstring.Bits(bytes=string_bytes)
    return string_bits.bin


def create_random(n, bits=True):
    """
    Create a random sequence of length n
    :param n: int
    :param bits: if True each item is a bit; else each item is a character
    :return: binary sequence or str
    """
    sequence = ""
    for i in range(0, n):
        sequence += str(random.getrandbits(1))
    if bits:
        string_bits = bitstring.BitArray(bin=sequence)
        return string_bits
    else:
        return sequence


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
    if len(a) != len(b):
        raise ValueError('Length mismatch!')
    if type(midpoint) is float:
        if not 0.0 <= midpoint <= 1.0:
            raise ValueError('Error in midpoint values!')
        new_sequence = a[0:int(len(a) * midpoint)]
        new_sequence += b[int(len(a) * (1 - midpoint)):]
    if type(midpoint) is int:
        if not 0 <= midpoint <= len(a):
            raise ValueError('Error in midpoint values!')
        new_sequence = a[0:midpoint]
        new_sequence += b[len(b) - midpoint:]
    return new_sequence


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
    copy = a[:]
    copy.invert(range(start, end))
    return copy


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
    copy = a[:]
    for i in range(start, end):
        if random.random() > pflip:
            copy.invert(i)
    return copy


def score_sequence(test, answer):
    """
    Scores a binary sequence against a correct sequence
    :raises ValueError if len(test) != len(answer)
    :param test: binary sequence
    :param answer: binary sequence
    :return: float [0,1]; (number of bits in test that match answer)/(number of bits in answer)
    """
    if len(test) != len(answer):
        raise ValueError('Length mismatch!')
    test_string, answer_string = test.bin, answer.bin
    score = 0
    for test_char, answer_char in zip(test_string, answer_string):
        if test_char == answer_char:
            score += 1
    return float(score / len(answer))


def probability_selection(population):
    """
    Selects a value from a population given a probability distribution
    :param population: iterable of tuples, where [1] is value and [0] is probability of selection
        probabilities must all be ints (relative frequency) or floats (likelihood), else raises ValueError
    :return: value of the selected item
    """
    probability_dist = []
    for i in range(0, len(population)):
        if type(population[i][0]) is not int and type(population[i][0]) is not float:
            raise ValueError('Probabilities must all be ints or floats!')
        if type(population[i][0]) is int:
            probability_type = "int"
            probability_dist.append(population[i][0])
        else:
            probability_type = "float"
            probability_dist.append(population[i][0])
    if probability_type is "int":
        total = sum(probability_dist)
        probability_dist[:] = [float(x / total) for x in probability_dist]
    return population[np.random.choice(range(0, len(population)), p=probability_dist)]


def ranked_selection(population):
    """
    Selects a value from a population prioritized by rank
    :param population: sorted iterable of current population
    :return: value of the selected item
    """
    return population[min(randint(0, len(population) - 1), randint(0, len(population) - 1))]


if __name__ == '__main__':
    import unittest


    class TestGAUtils(unittest.TestCase):
        def setUp(self):
            pass

        def test_str_to_bin(self):
            result = str_to_bin('foobar')
            self.assertEqual(len(result), 48)
            self.assertEqual(type(result), str)
            self.assertEqual(result, '011001100110111101101111011000100110000101110010')

        def test_create_random(self):
            result = create_random(8, True)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), bitstring.BitArray)

            result = create_random(8, False)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), str)

        def test_midpoint_xover(self):
            sequence_a = bitstring.BitArray(bin='00000000')
            sequence_b = bitstring.BitArray(bin='11111111')

            self.assertRaises(ValueError, lambda: midpoint_xover(bitstring.BitArray(bin='000000'),
                                                                 bitstring.BitArray(bin='00000000'), 0.5))

            self.assertRaises(ValueError, lambda: midpoint_xover(sequence_a, sequence_b, 1.1))
            self.assertRaises(ValueError, lambda: midpoint_xover(sequence_a, sequence_b, 10))

            result = midpoint_xover(sequence_a, sequence_b, 0.5)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), bitstring.BitArray)
            self.assertEqual(result.bin, '00001111')

            result = midpoint_xover(sequence_a, sequence_b, 4)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), bitstring.BitArray)
            self.assertEqual(result.bin, '00001111')

        def test_location_mutation(self):
            sequence = bitstring.BitArray(bin='00000000')

            result = location_mutation(sequence, 0, 4)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), bitstring.BitArray)
            self.assertEqual(result.bin, '11110000')

            result = location_mutation(sequence, 0, 0.5)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), bitstring.BitArray)
            self.assertEqual(result.bin, '11110000')

        def test_probability_mutation(self):
            sequence = bitstring.BitArray(bin='00000000')

            random.seed(1)
            result = probability_mutation(sequence, 0.5, 0, 4)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), bitstring.BitArray)
            self.assertEqual(result.bin, '01100000')

            random.seed(1)
            result = probability_mutation(sequence, 0.5, 0, 0.5)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), bitstring.BitArray)
            self.assertEqual(result.bin, '01100000')

        def test_score_sequence(self):
            sequence_a = bitstring.BitArray(bin='00000000')
            sequence_b = bitstring.BitArray(bin='11111111')
            sequence_c = bitstring.BitArray(bin='00001111')

            self.assertRaises(ValueError, lambda: score_sequence(bitstring.BitArray(bin='000000'),
                                                                 bitstring.BitArray(bin='00000000')))

            result = score_sequence(sequence_a, sequence_b)
            self.assertEqual(type(result), float)
            self.assertEqual(result, 0)

            result = score_sequence(sequence_b, sequence_c)
            self.assertEqual(type(result), float)
            self.assertEqual(result, 0.5)

        def test_probability_selection(self):
            population1 = [[0.1, 10], [0.1, 20], [0.1, 7], [0.7, 15]]
            population2 = [[10, 10], [10, 20], [10, 7], [70, 15]]

            self.assertRaises(ValueError, lambda: probability_selection(['notanint', 'notafloat']))

            np.random.seed(1)
            result = probability_selection(population1)
            self.assertEqual(type(result), list)
            self.assertEqual(result[1], 15)

            np.random.seed(1)
            result = probability_selection(population2)
            self.assertEqual(type(result), list)
            self.assertEqual(result[1], 15)

        def test_ranked_selection(self):
            # ISSUE Please confirm if I am testing this correctly.
            population1 = [[0.8, 10], [0.2, 20]]
            population2 = [[80, 10], [20, 20]]

            random.seed(1)
            result = probability_selection(population1)
            self.assertEqual(type(result), list)
            self.assertEqual(result[1], 10)

            random.seed(1)
            result = probability_selection(population2)
            self.assertEqual(type(result), list)
            self.assertEqual(result[1], 10)

        def tearDown(self):
            pass


    unittest.main(verbosity=2)
