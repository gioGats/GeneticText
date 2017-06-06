from bitstring import BitArray as Ba

from string import ascii_letters
from random import randint, choices, seed, random


class BitArray(Ba):
    def __lt__(self, other):
        return True


def str_to_bin(string):
    """
    Convert string to binary representation
    :param string: str to convert
    :return: BitArray
    """
    return BitArray(bytes=str.encode(string))


def bin_to_str(bin_sequence):
    """
    Converts a BitArray to a string
    :param bin_sequence: seq to convert
    :return: string
    """
    return bin_sequence.tobytes().decode('utf-8')


def create_random(n, bits=True):
    """
    Create a random sequence of length n
    :param n: int
    :param bits: if True each item is a bit; else each item is a character
    :return: BitArray or str
    """
    if bits:
        return BitArray(uint=randint(0, 2**n - 1), length=n)

    else:
        return ''.join(choices(ascii_letters, k=n))  #TODO Add uppercase, numbers, and symbols


def midpoint_xover(a, b, midpoint):
    """
    Do a midpoint crossover of a and b
    :raises ValueError if len(a) != len(b)
    :raises ValueError if midpoint is not [0.0, 1.0] or [0, len(a)]
    :raises TypeError if midpoint is not float or int
    :param a: BitArray
    :param b: BitArray
    :param midpoint: if float, take first midpoint percent of a and last (1-midpoint) percent of b
                     if int, take first midpoint items of a and last (length-midpoint) items of b
    :return: BitArray
    """
    if len(a) != len(b):
        raise ValueError('Length mismatch!')
    if isinstance(midpoint, float):
        if not 0.0 <= midpoint <= 1.0:
            raise ValueError('Error in midpoint values!')
        new_sequence = a[0:int(len(a) * midpoint)]
        new_sequence.append(b[int(len(a) * midpoint):])
    elif isinstance(midpoint, int):
        if not 0 <= midpoint <= len(a):
            raise ValueError('Error in midpoint values!')
        new_sequence = a[0:midpoint]
        new_sequence.append(b[midpoint:])
    else:
        raise TypeError('Midpoint must be float or int, is %s' % str(type(midpoint)))
    if len(new_sequence) != len(a):
        # print(a.bin, b.bin, midpoint, new_sequence.bin)
        raise ValueError('Mismatch in length values!')
    return new_sequence


def location_mutation(a, start=0, end=None):
    """
    Flips the bits of a between position start and position end
    :raises ValueError if start >= end
    :raises TypeError if start or end are not float or int
    :param a: BitArray
    :param start: int position (or float percentage) to start flipping
    :param end: int position (or float percentage) to stop flipping, set to len(a) if end is None.
    :return: BitArray
    """
    # Handle default
    if end is None:
        end = len(a)
    # Type Checking
    if not (isinstance(start, float) or isinstance(start, int)):
        raise TypeError('Start must be float or int, is %s' % str(type(start)))
    if not (isinstance(end, float) or isinstance(end, int)):
        raise TypeError('End must be float or int, is %s' % str(type(end)))
    if isinstance(start, float):
        start = int(min(max(start, 0.0), 1.0) * len(a))
    if isinstance(end, float):
        end = int(min(max(end, 0.0), 1.0) * len(a))
    if start < end:
        copy = a[:]
        copy.invert(range(start, end))
        return copy
    else:
        raise ValueError('Start(%.2f) >= End(%.2f)' % (float(start), float(end)))


def probability_mutation(a, pflip, start=0, end=None):
    """
    Flips the bits of a between position start and position end with probability pflip
    :param a: BitArray
    :param pflip: float (0,1); if random.random() > pflip, flip that bit
    :param start: int position (or float percentage) to start flipping
    :param end: int position (or float percentage) to stop flipping, set to len(a) if end is None.
    :return: BitArray
    """
    if isinstance(start, float):
        start = int(min(max(start, 0.0), 1.0) * len(a))
    if isinstance(end, float):
        end = int(min(max(end, 0.0), 1.0) * len(a))
    elif end is None:
        end = len(a)
    assert start < end
    copy = a[:]
    # FUTURE Do this without a 'for' loop or make it parallel

    flip_list = []
    for i in range(start, end):
        if random() > pflip:
            flip_list.append(i)

    copy.invert(flip_list)
    return copy


def score_sequence(test, answer):
    """
    Scores a BitArray against a correct sequence
    :raises ValueError if len(test) != len(answer)
    :param test: BitArray
    :param answer: BitArray
    :return: float [0,1]; (number of bits in test that match answer)/(number of bits in answer)
    """
    if len(test) != len(answer):
        raise ValueError('Length mismatch: test(%d) != answer(%d)' % (len(test), len(answer)))
    test_string, answer_string = test.bin, answer.bin
    score = 0
    # FUTURE Do this without a 'for' loop or make it parallel
    for test_char, answer_char in zip(test_string, answer_string):
        if test_char == answer_char:
            score += 1
    return float(score / len(answer))


def probability_selection(pop_score_list):
    """
    Selects a value from a population given a probability distribution
    :param pop_score_list: iterable of tuples, where [1] is value and [0] is probability of selection
        probabilities must all be ints (relative frequency) or floats (likelihood), else raises ValueError
    :return: value of the selected item
    """
    # FUTURE Add type checking (all ints or all floats)
    probability_dist = []
    for i in range(0, len(pop_score_list)):
        if type(pop_score_list[i][0]) is not int and type(pop_score_list[i][0]) is not float:
            raise ValueError('Probabilities must all be ints or floats!')
        if type(pop_score_list[i][0]) is int:
            probability_type = "int"
            probability_dist.append(pop_score_list[i][0])
        else:
            probability_type = "float"
            probability_dist.append(pop_score_list[i][0])
    if probability_type is "int":
        total = sum(probability_dist)
        probability_dist[:] = [float(x / total) for x in probability_dist]  # FUTURE Vectorize this

    return pop_score_list[choices(range(0, len(pop_score_list)), weights=probability_dist, k=1)[0]][1]


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
            self.assertEqual(type(result), BitArray)
            self.assertEqual(result.bin, '011001100110111101101111011000100110000101110010')
            self.assertEqual(str_to_bin(bin_to_str(BitArray(bin='01010000'))).bin, '01010000')

        def test_bin_to_str(self):
            result = bin_to_str(BitArray(bin='011001100110111101101111011000100110000101110010'))
            self.assertEqual(len(result), 6)
            self.assertEqual(type(result), str)
            self.assertEqual(result, 'foobar')
            self.assertEqual(bin_to_str(str_to_bin('fubar')), 'fubar')

        def test_create_random(self):
            result = create_random(64, True)
            self.assertEqual(len(result), 64)
            self.assertEqual(type(result), BitArray)

            result = create_random(8, False)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), str)

        def test_midpoint_xover(self):
            sequence_a = BitArray(bin='00000000')
            sequence_b = BitArray(bin='11111111')

            self.assertRaises(ValueError, lambda: midpoint_xover(BitArray(bin='000000'),
                                                                 BitArray(bin='00000000'), 0.5))

            self.assertRaises(ValueError, lambda: midpoint_xover(sequence_a, sequence_b, 1.1))
            self.assertRaises(ValueError, lambda: midpoint_xover(sequence_a, sequence_b, 10))

            result = midpoint_xover(sequence_a, sequence_b, 0.5)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), BitArray)
            self.assertEqual(result.bin, '00001111')

            result = midpoint_xover(sequence_a, sequence_b, 4)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), BitArray)
            self.assertEqual(result.bin, '00001111')

        def test_location_mutation(self):
            sequence = BitArray(bin='00000000')

            result = location_mutation(sequence, 0, 4)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), BitArray)
            self.assertEqual(result.bin, '11110000')

            result = location_mutation(sequence, 0, 0.5)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), BitArray)
            self.assertEqual(result.bin, '11110000')

        def test_probability_mutation(self):
            sequence = BitArray(bin='00000000')

            seed(1)
            result = probability_mutation(sequence, 0.5, 0, 4)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), BitArray)
            self.assertEqual(result.bin, '01100000')

            seed(1)
            result = probability_mutation(sequence, 0.5, 0, 0.5)
            self.assertEqual(len(result), 8)
            self.assertEqual(type(result), BitArray)
            self.assertEqual(result.bin, '01100000')

        def test_score_sequence(self):
            sequence_a = BitArray(bin='00000000')
            sequence_b = BitArray(bin='11111111')
            sequence_c = BitArray(bin='00001111')

            self.assertRaises(ValueError, lambda: score_sequence(BitArray(bin='000000'),
                                                                 BitArray(bin='00000000')))

            result = score_sequence(sequence_a, sequence_b)
            self.assertEqual(type(result), float)
            self.assertEqual(result, 0)

            result = score_sequence(sequence_b, sequence_c)
            self.assertEqual(type(result), float)
            self.assertEqual(result, 0.5)

        def test_probability_selection(self):
            # FUTURE The function is ambiguous as to the type of the actual value,
            # but in this case, it will be a function from generation_functions
            population1 = [[0.1, BitArray(bin='00000001')], [0.1, BitArray(bin='00000011')],
                           [0.1, BitArray(bin='00000111')], [0.7, BitArray(bin='00001111')]]
            population2 = [[10, BitArray(bin='00011111')], [10, BitArray(bin='00111111')],
                           [10, BitArray(bin='01111111')], [70, BitArray(bin='11111111')]]

            self.assertRaises(ValueError, lambda: probability_selection(['notanint', 'notafloat']))

            seed(1)
            result = probability_selection(population1)
            self.assertEqual(type(result), type(population1[0][1]))
            self.assertEqual(result.bin, '00000011')

            seed(1)
            result = probability_selection(population2)
            self.assertEqual(type(result), type(population2[0][1]))
            self.assertEqual(result.bin, '00111111')

        def test_ranked_selection(self):
            population1 = [BitArray(bin='00000001'), BitArray(bin='11111111')]
            population2 = [BitArray(bin='00000000'), BitArray(bin='11111110')]

            seed(1)
            result = ranked_selection(population1)
            self.assertEqual(type(result), BitArray)
            self.assertEqual(result.bin, '00000001')

            seed(1)
            result = ranked_selection(population2)
            self.assertEqual(type(result), BitArray)
            self.assertEqual(result.bin, '00000000')

        def tearDown(self):
            pass


    unittest.main(verbosity=2)
