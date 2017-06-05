from ga_utils import *
from random import randint, gauss, random, seed


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
            population = [BitArray(bin='00000001'), BitArray(bin='00000011'),
                          BitArray(bin='00000111'), BitArray(bin='00001111'),
                          BitArray(bin='00011111'), BitArray(bin='00111111'),
                          BitArray(bin='01111111'), BitArray(bin='11111111')]

            self.assertRaises(ValueError, lambda: generate_xover(population, midpoint_dist='error'))

            seed(1)

            uniform_xover = generate_xover(population, midpoint_dist='uniform')
            normal_xover = generate_xover(population, midpoint_dist='normal')

            self.assertEqual(type(uniform_xover), BitArray)
            self.assertEqual(uniform_xover.bin, '00000011')
            self.assertEqual(type(normal_xover), BitArray)
            self.assertEqual(normal_xover.bin, '00000011')

        def test_generate_lmutate(self):
            population = [BitArray(bin='00000001'), BitArray(bin='00000011'),
                          BitArray(bin='00000111'), BitArray(bin='00001111'),
                          BitArray(bin='00011111'), BitArray(bin='00111111'),
                          BitArray(bin='01111111'), BitArray(bin='11111111')]

            self.assertRaises(ValueError, lambda: generate_lmutate(population, locate_dist='error'))

            seed(1)

            uniform_lmutate = generate_lmutate(population, locate_dist='uniform')
            normal_lmutate = generate_lmutate(population, locate_dist='normal')

            self.assertEqual(type(uniform_lmutate), BitArray)
            self.assertEqual(uniform_lmutate.bin, '01000011')
            self.assertEqual(type(normal_lmutate), BitArray)
            self.assertEqual(normal_lmutate.bin, '11111111')

        def test_generate_pmutate(self):
            population = [BitArray(bin='00000001'), BitArray(bin='00000011'),
                          BitArray(bin='00000111'), BitArray(bin='00001111'),
                          BitArray(bin='00011111'), BitArray(bin='00111111'),
                          BitArray(bin='01111111'), BitArray(bin='11111111')]

            self.assertRaises(ValueError,
                              lambda: generate_pmutate(population, locate_dist='error', pflip_dist='uniform'))
            self.assertRaises(ValueError,
                              lambda: generate_pmutate(population, locate_dist='uniform', pflip_dist='error'))

            seed(2)

            uu_pmutate = generate_pmutate(population, locate_dist='uniform', pflip_dist='uniform')
            un_pmutate = generate_pmutate(population, locate_dist='uniform', pflip_dist='normal')

            nu_pmutate = generate_pmutate(population, locate_dist='normal', pflip_dist='uniform')
            nn_pmutate = generate_pmutate(population, locate_dist='normal', pflip_dist='normal')

            self.assertEqual(type(uu_pmutate), BitArray)
            self.assertEqual(uu_pmutate.bin, '10000111')
            self.assertEqual(type(un_pmutate), BitArray)
            self.assertEqual(un_pmutate.bin, '10011111')
            self.assertEqual(type(nu_pmutate), BitArray)
            self.assertEqual(nu_pmutate.bin, '01000001')
            self.assertEqual(type(nn_pmutate), BitArray)
            self.assertEqual(nn_pmutate.bin, '00000110')

        def tearDown(self):
            pass


    unittest.main(verbosity=2)
