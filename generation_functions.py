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
            population = [bitstring.BitArray(bin='00000001'), bitstring.BitArray(bin='00000011'),
                          bitstring.BitArray(bin='00000111'), bitstring.BitArray(bin='00001111'),
                          bitstring.BitArray(bin='00011111'), bitstring.BitArray(bin='00111111'),
                          bitstring.BitArray(bin='01111111'), bitstring.BitArray(bin='11111111')]

            self.assertRaises(ValueError, lambda: generate_xover(population, midpoint_dist='error'))

            uniform_xover = generate_xover(population, midpoint_dist='uniform')
            normal_xover = generate_xover(population, midpoint_dist='normal')

            self.assertEqual(type(uniform_xover), bitstring.BitArray)
            self.assertEqual(type(normal_xover), bitstring.BitArray)

            # TODO Can we add some value verification here? (probably using a designated random seed)

        def test_generate_lmutate(self):
            population = [bitstring.BitArray(bin='00000001'), bitstring.BitArray(bin='00000011'),
                          bitstring.BitArray(bin='00000111'), bitstring.BitArray(bin='00001111'),
                          bitstring.BitArray(bin='00011111'), bitstring.BitArray(bin='00111111'),
                          bitstring.BitArray(bin='01111111'), bitstring.BitArray(bin='11111111')]

            self.assertRaises(ValueError, lambda: generate_lmutate(population, locate_dist='error'))

            uniform_lmutate = generate_lmutate(population, locate_dist='uniform')
            normal_lmutate = generate_lmutate(population, locate_dist='normal')

            self.assertEqual(type(uniform_lmutate), bitstring.BitArray)
            self.assertEqual(type(normal_lmutate), bitstring.BitArray)

            # TODO Can we add some value verification here? (probably using a designated random seed)

        def test_generate_pmutate(self):
            population = [bitstring.BitArray(bin='00000001'), bitstring.BitArray(bin='00000011'),
                          bitstring.BitArray(bin='00000111'), bitstring.BitArray(bin='00001111'),
                          bitstring.BitArray(bin='00011111'), bitstring.BitArray(bin='00111111'),
                          bitstring.BitArray(bin='01111111'), bitstring.BitArray(bin='11111111')]

            self.assertRaises(ValueError,
                              lambda: generate_pmutate(population, locate_dist='error', pflip_dist='uniform'))
            self.assertRaises(ValueError,
                              lambda: generate_pmutate(population, locate_dist='uniform', pflip_dist='error'))

            uu_pmutate = generate_pmutate(population, locate_dist='uniform', pflip_dist='uniform')
            un_pmutate = generate_pmutate(population, locate_dist='uniform', pflip_dist='normal')

            nu_pmutate = generate_pmutate(population, locate_dist='normal', pflip_dist='uniform')
            nn_pmutate = generate_pmutate(population, locate_dist='normal', pflip_dist='normal')

            self.assertEqual(type(uu_pmutate), bitstring.BitArray)
            self.assertEqual(type(un_pmutate), bitstring.BitArray)
            self.assertEqual(type(nu_pmutate), bitstring.BitArray)
            self.assertEqual(type(nn_pmutate), bitstring.BitArray)

            # TODO Can we add some value verification here? (probably using a designated random seed)


        def tearDown(self):
            pass


    unittest.main(verbosity=2)
