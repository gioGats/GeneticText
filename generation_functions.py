from ga_utils import *
from random import randint, gauss, random


def generate_xover(population, midpoint_dist='uniform'):
    """
    Generates a new value using crossover mutation
    :param population: sorted iterable of current population
    :param midpoint_dist: 'uniform' or 'normal' distributions for selecting midpoint
    :return: new value
    """
    if midpoint_dist is 'uniform':
        midpoint = randint(0, len(population[0]))
    elif midpoint_dist is 'normal':
        midpoint = max(min(int(gauss(0.5 * len(population[0]), 0.5 * len(population[0]))), len(population[0])), 0)
    else:
        raise ValueError('Midpoint distribution must be uniform or normal')

    mom, dad = ranked_selection(population), ranked_selection(population)
    return midpoint_xover(mom, dad, midpoint)


def generate_lmutate(population, locate_dist='uniform'):
    """
    Generates a new value using location mutation
    :param population: sorted iterable of current population
    :param locate_dist: 'uniform' or 'normal' distributions for selecting locations
    :return: new value
    """
    if locate_dist is 'uniform':
        a = randint(0, len(population[0]))
        b = randint(0, len(population[0]))
    elif locate_dist is 'normal':
        a = max(min(int(gauss(0.5 * len(population[0]), 0.5 * len(population[0]))), len(population[0])), 0)
        b = max(min(int(gauss(0.5 * len(population[0]), 0.5 * len(population[0]))), len(population[0])), 0)
    else:
        raise ValueError('Location distribution must be uniform or normal')
    return location_mutation(ranked_selection(population), min(a, b), max(a, b))


def generate_pmutate(population, locate_dist='uniform', pflip_dist='uniform'):
    """
    Generates a new value using location mutation
    :param population: sorted iterable of current population
    :param locate_dist: 'uniform' or 'normal' distributions for selecting locations
    :param pflip_dist: 'uniform' or 'normal' distributions for selecting pflip
    :return: new value
    """
    if locate_dist is 'uniform':
        a = randint(0, len(population[0]))
        b = randint(0, len(population[0]))
    elif locate_dist is 'normal':
        a = max(min(int(gauss(0.5 * len(population[0]), 0.5 * len(population[0]))), len(population[0])), 0)
        b = max(min(int(gauss(0.5 * len(population[0]), 0.5 * len(population[0]))), len(population[0])), 0)
    else:
        raise ValueError('Location distribution must be uniform or normal')
    if pflip_dist is 'uniform':
        p = random()
    elif pflip_dist is 'normal':
        p = max(min(gauss(0.5, 0.5), 1.0), 0.0)
    else:
        raise ValueError('Pflip distribution must be uniform or normal')
    return probability_mutation(ranked_selection(population), p, min(a, b), max(a, b))


if __name__ == '__main__':
    import unittest

    class TestGenFns(unittest.TestCase):
        def setUp(self):
            pass

        def test_generate_xover(self):
            # TODO Implement test_generate_xover
            population = [[0.8, bitstring.BitArray(bin='00000001')], [0.2, bitstring.BitArray(bin='11111111')]]
            #population2 = [[10, 10], [10, 20], [10, 7], [70, 15]]

            self.assertRaises(ValueError, lambda: generate_xover(population, midpoint_dist='foobar'))
            uniform_xover = generate_xover(population, midpoint_dist='uniform')
            normal_xover = generate_xover(population, midpoint_dist='normal')

            print(uniform_xover)
            print(normal_xover)

            # self.assertEqual(test_result.shape, (5,))
            # self.assertEqual(test_result.dtype, np.float32)
            # np.testing.assert_array_equal(test_result, solution)

        def test_generate_lmutate(self):
            # TODO Implement test_generate_lmutate
            self.fail('Not implemented')

        def test_generate_pmutate(self):
            # TODO Implement test_generate_pmutate
            self.fail('Not implemented')

        def tearDown(self):
            pass

    unittest.main(verbosity=2)