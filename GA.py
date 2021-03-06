from ga_utils import *
from generation_functions import *

from time import time
from os import makedirs
from datetime import datetime
from sys import getsizeof

import unittest


class GeneticAlgorithm(object):
    def __init__(self, pop_size, generations):
        """
        :param pop_size: int
        :param generations: int
        """
        self._pop_size = pop_size
        self._generations = generations

        # Initially undefined attributes
        self._target_text = None
        self._target = None
        self._chromosome_length = None
        self._generate_functions = []
        self._current_pop = None
        self._current_pop_scores = None
        self._next_pop = None

    def set_target(self, target_text):
        """
        :param target_text: str
        """
        self._target_text = target_text
        self._target = str_to_bin(target_text)
        self._chromosome_length = len(self._target)
        self._current_pop = []
        self._current_pop_scores = []
        self._next_pop = []

    def add_generation_function(self, function, probability):
        """
        :param function: callable
        :param probability: int or float
        """
        self._generate_functions.append([probability, function])

    def default_generation_functions(self):
        for fn in [generate_xover, generate_lmutate, generate_pmutate]:  # FUTURE Use lambdas to strip default params
            self.add_generation_function(fn, 1)

    def sort_current_pop(self):
        """
        Sorts _current_pop and _current_pop_scores in descending order based on _current_pop_scores.
        """
        # Must be efficient
        # FUTURE Ryan check efficiency (elevate to T.ODO when unittest complete)
        self._current_pop, self._current_pop_scores = \
            [x for (y, x) in sorted(zip(self._current_pop_scores, self._current_pop))][::-1], \
            [y for (y, x) in sorted(zip(self._current_pop_scores, self._current_pop))][::-1]

    def score_current_pop(self):
        """
        Assigns scores for items in _current_pop to the same index in _current_pop_scores.
        """

        # Must be efficient
        # FUTURE Ryan check efficiency (elevate to T.ODO when unittest complete)
        self._current_pop_scores = []
        for i in self._current_pop:
            self._current_pop_scores.append(score_sequence(i, self._target))
        self._current_pop_scores = self._current_pop_scores
        """
        self._current_pop_scores = self._current_pop[:]
        for i in range(0, len(self._current_pop)):
            temp_list = []
            for j in range(0, len(self._current_pop[i])):
                temp_list.append(score_sequence(self._current_pop[i][j], self._target))
            self._current_pop_scores[i] = tuple(temp_list)
        """

    @property
    def best_candidate(self):
        return self._current_pop[0]

    @property
    def best_candidate_score(self):
        return self._current_pop_scores[0]

    def run(self, verbosity=1, max_time=float('+inf'), min_convergence=float('-inf')):
        if None in [self._target_text, self._target, self._generate_functions, self._current_pop, self._next_pop]:
            raise AttributeError('Initialization attributes must be defined before running genetic algorithm.')
        if not self._generate_functions:  # Default generation functions
            self.default_generation_functions()

        # Init of loop tracking variables
        iteration_count = 0
        start_time = time()
        start_dtg = str(datetime.now()).replace(' ', '_')

        while True:
            # GENERATION
            if iteration_count == 0:  # Special first iteration
                last_best = 0.0
                self._current_pop = []
                for i in range(self._pop_size):
                    self._current_pop.append(create_random(len(self._target_text), bits=True))
                    # FUTURE Vectorize or parallel
            else:
                last_best = self.best_candidate_score
                self._next_pop = []
                for i in range(self._pop_size):
                    """ Breakout for testing
                    gen_fn = probability_selection(self._generate_functions)
                    # print(gen_fn.__name__)
                    new_birth = gen_fn(self._current_pop)
                    assert(len(new_birth) == self._chromosome_length)
                    self._next_pop.append(new_birth)
                    """
                    self._next_pop.append(probability_selection(self._generate_functions)(self._current_pop))
                    # FUTURE Vectorize or parallel

                assert len(self._current_pop) == len(self._next_pop)
                self._current_pop = self._next_pop

            # SCORING
            self.score_current_pop()
            self.sort_current_pop()
            improvement = self.best_candidate_score - last_best

            # REPORTING
            if verbosity >= 1:
                print('\rIteration %8d | Best score: %.8f | Improvement: %.8f' %
                      (iteration_count, self.best_candidate_score, improvement), end='')
            if verbosity >= 2 and iteration_count % 10 == 0:
                makedirs('checkpoints/%s' % str(start_dtg))
                with open('checkpoints/%s/%d.txt' % (str(start_dtg), iteration_count), 'w') as f:
                    f.write('Iteration %8d | Best score: %.8f | Improvement: %.8f\n' %
                            (iteration_count, self.best_candidate_score, improvement))
                    f.write(bin_to_str(self.best_candidate))
                    if verbosity >= 3:
                        f.write(self.best_candidate)

            # TERMINATION
            if iteration_count > self._generations:  # Max iterations
                break
            elif self.best_candidate_score == 1.0:  # Perfection
                break
            elif (improvement < min_convergence) and iteration_count != 0:  # Convergence
                break
            elif time() - start_time > max_time:  # Time
                break
            else:
                iteration_count += 1


class TestGeneticAlgorithm(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        ga = GeneticAlgorithm(pop_size=8, generations=4)

        self.assertEqual(type(ga._pop_size), int)
        self.assertEqual(ga._pop_size, 8)
        self.assertEqual(type(ga._generations), int)
        self.assertEqual(ga._generations, 4)
        self.assertEqual(type(ga._generate_functions), list)
        self.assertEqual(ga._generate_functions, [])
        self.assertEqual(ga._target_text, None)
        self.assertEqual(ga._target, None)
        self.assertEqual(ga._chromosome_length, None)
        self.assertEqual(ga._current_pop, None)
        self.assertEqual(ga._current_pop_scores, None)
        self.assertEqual(ga._next_pop, None)

    def test_set_target(self):
        ga = GeneticAlgorithm(pop_size=8, generations=4)
        ga.set_target('hi')

        self.assertEqual(ga._target_text, 'hi')
        self.assertEqual(type(ga._target_text), str)
        self.assertEqual(ga._target.bin, '0110100001101001')
        self.assertEqual(type(ga._target), BitArray)
        self.assertEqual(ga._chromosome_length, 16)
        self.assertEqual(type(ga._chromosome_length), int)
        self.assertEqual(type(ga._current_pop), list)
        self.assertEqual(type(ga._current_pop_scores), list)
        self.assertEqual(type(ga._next_pop), list)

    def test_sort_current_pop(self):
        ga = GeneticAlgorithm(pop_size=4, generations=4)
        ga._current_pop = [
            BitArray(bin='0000'), BitArray(bin='1111'), BitArray(bin='1001'),
            BitArray(bin='0110'),
            BitArray(bin='0001'), BitArray(bin='0011'), BitArray(bin='0111'),
            BitArray(bin='1110')]

        solution = ga._current_pop[::-1]

        ga._current_pop_scores = [1., 2., 3., 4., 5., 6., 7., 8.]
        solution_scores = ga._current_pop_scores[::-1]

        ga.sort_current_pop()

        self.assertEqual(ga._current_pop, solution)
        self.assertEqual(type(ga._current_pop), list)
        self.assertEqual(type(ga._current_pop[0]), BitArray)
        self.assertEqual(ga._current_pop_scores, solution_scores)
        self.assertEqual(type(ga._current_pop_scores), list)
        self.assertEqual(type(ga._current_pop_scores[0]), float)

    def test_score_current_pop(self):
        ga = GeneticAlgorithm(pop_size=4, generations=4)
        ga._target = BitArray(bin='0000')
        ga._current_pop = [
            BitArray(bin='0000'), BitArray(bin='1111'), BitArray(bin='1001'),
            BitArray(bin='0110'),
            BitArray(bin='0001'), BitArray(bin='0011'), BitArray(bin='0111'),
            BitArray(bin='1110')]

        solution_scores = [1.0, 0, 0.5, 0.5, 0.75, 0.5, 0.25, 0.25]

        ga.score_current_pop()

        self.assertEqual(ga._current_pop_scores, solution_scores)
        self.assertEqual(type(ga._current_pop), list)
        self.assertEqual(type(ga._current_pop[0]), BitArray)
        self.assertEqual(ga._target, BitArray(bin='0000'))
        self.assertEqual(type(ga._current_pop_scores), list)
        self.assertEqual(type(ga._current_pop_scores[0]), float)

    def test_best_candidate(self):
        ga = GeneticAlgorithm(pop_size=4, generations=4)
        ga._current_pop = [
            BitArray(bin='0000'), BitArray(bin='1111'), BitArray(bin='1001'),
            BitArray(bin='0110'),
            BitArray(bin='0001'), BitArray(bin='0011'), BitArray(bin='0111'),
            BitArray(bin='1110')]

        solution = ga.best_candidate

        self.assertEqual(ga._current_pop[0], solution)
        self.assertEqual(type(solution), BitArray)

    def test_best_candidate_score(self):
        ga = GeneticAlgorithm(pop_size=4, generations=4)
        ga._current_pop_scores = [1.0, 0, 0.5, 0.5, 0.75, 0.5, 0.25, 0.25]

        solution = ga.best_candidate_score

        self.assertEqual(ga._current_pop_scores[0], solution)
        self.assertEqual(type(solution), float)

    def test_ga_utils_correctness(self):
        ga_utils_arr = [create_random(1, bits=True) for i in range(10)]
        ga_utils_scores = []
        selections = []

        for i in range(0, 10):
            # bin to str
            ga_utils_str = bin_to_str(ga_utils_arr[i])
            self.assertEqual(len(ga_utils_str), 1)
            self.assertEqual(type(ga_utils_str), str)

            # str to bin
            ga_utils_bin = str_to_bin(ga_utils_str)
            self.assertEqual(len(ga_utils_bin), 8)
            self.assertEqual(type(ga_utils_bin), BitArray)
            self.assertEqual(ga_utils_bin, ga_utils_arr[i])

            # midpoint xover
            if i != 9:
                ga_utils_xover = midpoint_xover(ga_utils_arr[i], ga_utils_arr[i + 1], 4)
                self.assertEqual(ga_utils_xover[0:4], ga_utils_arr[i][0:4])
                self.assertEqual(ga_utils_xover[4:8], ga_utils_arr[i + 1][4:8])
            else:
                ga_utils_xover = midpoint_xover(ga_utils_arr[i], ga_utils_arr[0], 4)
                self.assertEqual(ga_utils_xover[0:4], ga_utils_arr[i][0:4])
                self.assertEqual(ga_utils_xover[4:8], ga_utils_arr[0][4:8])

            self.assertEqual(len(ga_utils_xover), 8)
            self.assertEqual(type(ga_utils_xover), BitArray)

            # location mutation
            lmutate_check = ga_utils_arr[i][:]
            lmutate_check.invert(range(0, 4))
            ga_utils_lmutate = location_mutation(ga_utils_arr[i], 0, 0.5)
            self.assertEqual(len(ga_utils_lmutate), 8)
            self.assertEqual(type(ga_utils_lmutate), BitArray)
            self.assertEqual(ga_utils_lmutate.bin, lmutate_check.bin)

            # probability mutation
            pmutate_check = ga_utils_arr[i][:]
            pmutate_check.invert([1, 2])
            seed(1)
            ga_utils_pmutate = probability_mutation(ga_utils_arr[i], 0.5, 0, 0.5)
            self.assertEqual(len(ga_utils_pmutate), 8)
            self.assertEqual(type(ga_utils_pmutate), BitArray)
            self.assertEqual(ga_utils_pmutate.bin, pmutate_check.bin)

            # score sequence
            ga_utils_score = score_sequence(ga_utils_arr[i], BitArray(bin='01111110'))
            self.assertEqual(type(ga_utils_score), float)
            ga_utils_scores.append(ga_utils_score)

            # probability selection setup
            selections.append([random(), ga_utils_arr[i]])

        # probability selection
        ga_utils_pselection = probability_selection(selections)
        self.assertEqual(len(ga_utils_pselection), 8)
        self.assertEqual(type(ga_utils_pselection), BitArray)

        # ranked selection
        ga_utils_arr, ga_utils_scores = \
            [x for (y, x) in sorted(zip(ga_utils_scores, ga_utils_arr))][::-1], \
            [y for (y, x) in sorted(zip(ga_utils_scores, ga_utils_arr))][::-1]
        ga_utils_rselection = ranked_selection(ga_utils_arr)
        self.assertEqual(len(ga_utils_rselection), 8)
        self.assertEqual(type(ga_utils_rselection), BitArray)

    def test_ga_performance(self):
        # FUTURE Upgrade to exponential regression for order of growth calculation
        from random import choices
        from string import ascii_letters
        for x in range(11, 16 + 1):
            ga = GeneticAlgorithm(pop_size=10, generations=10)
            ga.set_target(create_random(2 ** x, bits=False))
            start = time()
            ga.run(verbosity=1)
            this_time = time() - start
            this_memory = getsizeof(ga)
            print(' | Factor: %d | Time %.4f seconds | Memory %.4f MB' % (x, this_time, (this_memory / 1000)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
