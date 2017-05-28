from ga_utils import *
from generation_functions import *

from time import time
from os import makedirs
from datetime import datetime


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
        # ISSUE See np_bs_issue.py
        self._current_pop = np.empty(shape=(self._pop_size, len(self._target)))
        self._current_pop_scores = np.empty(shape=(self._pop_size,))
        self._next_pop = np.empty(shape=(self._pop_size, len(self._target)))

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
        base = self._current_pop_scores.argsort()[::-1]
        self._current_pop = self._current_pop[:, base]
        self._current_pop_scores = self._current_pop_scores[base]

    def score_current_pop(self):
        """
        Assigns scores for items in _current_pop to the same index in _current_pop_scores.
        """

        # Must be efficient
        # FUTURE Ryan check efficiency (elevate to T.ODO when unittest complete)
        def score(x):
            return score_sequence(x, self._target)

        v_func = np.vectorize(score)
        self._current_pop_scores = v_func(self._current_pop)

    @property
    def best_candidate(self):
        return self._current_pop[0]

    @property
    def best_candidate_score(self):
        return self._current_pop_scores[0]

    def run(self, verbosity=1, max_iterations=float('inf'), max_time=float('inf'), min_convergence=0.0):
        if None in [self._target_text, self._target, self._generate_functions, self._current_pop, self._next_pop]:
            raise AttributeError('Initialization attributes must be defined before running genetic algorithm.')
        if not self._generate_functions:  # Default generation functions
            self.default_generation_functions()

        # Init of loop tracking variables
        iteration_count = 0
        start_time = time()
        start_dtg = str(datetime.now()).replace(' ', '_')

        while True:
            last_best = self.best_candidate_score
            # GENERATION
            if iteration_count == 0:  # Special first iteration
                for i in range(len(self._current_pop)):
                    self._current_pop[i] = create_random(self._chromosome_length, bits=True)
                    # FUTURE Vectorize or parallel
            else:
                assert len(self._current_pop) == len(self._next_pop)
                for i in range(len(self._current_pop)):
                    self._next_pop = probability_selection(self._generate_functions)(self._current_pop)
                    # FUTURE Vectorize or parallel
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
            if iteration_count > max_iterations:  # Max iterations
                break
            elif self.best_candidate_score == 1.0:  # Perfection
                break
            elif (improvement < min_convergence) and iteration_count != 0:  # Convergence
                break
            elif time() - start_time > max_time:  # Time
                break
            else:
                iteration_count += 1


if __name__ == '__main__':
    # TODO Implement a unittest.TestCase for GeneticAlgorithm and test the methods:
    import unittest


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
            self.assertEqual(type(ga._target), bitstring.BitArray)
            self.assertEqual(ga._chromosome_length, 16)
            self.assertEqual(type(ga._chromosome_length), int)
            self.assertEqual(ga._current_pop.shape, (8, 16))
            self.assertEqual(type(ga._current_pop), np.ndarray)
            self.assertEqual(ga._current_pop_scores.shape, (8,))
            self.assertEqual(type(ga._current_pop_scores), np.ndarray)
            self.assertEqual(ga._next_pop.shape, (8, 16))
            self.assertEqual(type(ga._next_pop), np.ndarray)

        def test_sort_current_pop(self):
            ga = GeneticAlgorithm(pop_size=8, generations=4)
            ga._current_pop = np.array(
                [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], ['i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']])
            ga._current_pop_scores = np.arange(1, 9)
            ga.sort_current_pop()

            np.testing.assert_array_equal(ga._current_pop, np.array(
                [['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'], ['p', 'o', 'n', 'm', 'l', 'k', 'j', 'i']]))
            self.assertEqual(type(ga._current_pop), np.ndarray)
            np.testing.assert_array_equal(ga._current_pop_scores, np.array(
                [8, 7, 6, 5, 4, 3, 2, 1]))
            self.assertEqual(type(ga._current_pop_scores), np.ndarray)
            # ISSUE Ryan, please verify that this is the correct equals value

        def test_score_current_pop(self):
            ga = GeneticAlgorithm(pop_size=4, generations=4)
            ga._target = bitstring.BitArray(bin='0000')
            ga._current_pop = np.array(
                [[bitstring.BitArray(bin='0000'), bitstring.BitArray(bin='1111'), bitstring.BitArray(bin='1001'),
                  bitstring.BitArray(bin='0110')],
                 [bitstring.BitArray(bin='0001'), bitstring.BitArray(bin='0011'), bitstring.BitArray(bin='0111'),
                  bitstring.BitArray(bin='1110')]], dtype=bitstring.BitArray)
            print(ga._current_pop)
            ga.score_current_pop()

            np.testing.assert_array_equal(ga._current_pop_scores, np.array(
                [8, 7, 6, 5, 4, 3, 2, 1]))
            self.assertEqual(type(ga._current_pop_scores), np.ndarray)

        def test_best_candidate(self):
            # TODO implement test_best_candidate
            self.fail('Not implemented')

        def test_best_candidate_score(self):
            # TODO implement test_best_candidate_score
            self.fail('Not implemented')

        def test_ga_utils_correctness(self):
            # TODO Create an empty array
            # TODO Use ga_utils to fill that array with randoms
            # TODO Can ga_utils functions still pass their tests when given the items from this array?
            # i.e. Do they fail when given np.array(dtype=np.bool) instead of a bitstring.BitArray?
            self.fail('Not implemented')

        def test_ga_utils_performance(self):
            # TODO Create an empty array
            # TODO Use ga_utils to fill that array with randoms
            # Most of these tests can initially just be a printout that we review manually
            # In the FUTURE automate tests to verify scaled performance meets a scaling standard
            # TODO Test performance, something akin to:
            """
            for function in ga_utils:
                run that function for every item in the array
                calculate an estimated runtime per item
                compare to the runtime of a single bitstring not involving numpy
                are these comparable?
            """
            # TODO Test size performance, something akin to:
            """
            define a large collection of bits, a (remember 8,000 bits equals ~1KB, this should probably be ~100KB)
            turn a into a BitArray, b, measure it's size.
            turn b into a numpy array, c, measure it's size.
            drop a into an empty numpy array (dtype=np.bool), d, and measure it's size
            drop a into an emtpy numpy array (dtype=np.float64), e, and measure it's size

            are b, c, and d comparable in size?
            is e 8 times the size of d (implying that numpy stores each bit as a byte) or
            is e 64 times the size of d (implying that numpy stores each bit as a bit)
            """
            self.fail('Not implemented')


    unittest.main(verbosity=2)
