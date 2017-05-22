from ga_utils import *
from generation_functions import *

from time import time
from os import makedirs
from datetime import datetime


class GeneticAlgorithm(object):
    def __init__(self, pop_size, generations):
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
        self._target_text = target_text
        self._target = str_to_bin(target_text)
        self._chromosome_length = len(self._target)
        self._current_pop = None  # TODO Set to an empty array of size (_pop_size, len(_target))
        self._current_pop_scores = None  # TODO Set to an empty array of size (_pop_size,)
        self._next_pop = None  # TODO Set to an empty array of size (_pop_size, len(_target))

    def add_generation_function(self, function, probability):
        self._generate_functions.append([probability, function])

    def default_generation_functions(self):
        for fn in [generate_xover, generate_lmutate, generate_pmutate]:  # FUTURE Use lambdas to strip default params
            self.add_generation_function(fn, 1)

    def sort_current_pop(self):
        """
        Sorts _current_pop and _current_pop_scores in descending order based on _current_pop_scores.
        """
        # TODO Implement sort_current_pop
        # Must be efficient
        raise NotImplementedError

    def score_current_pop(self):
        """
        Assigns scores for items in _current_pop to the same index in _current_pop_scores.
        """
        # TODO Implement score_current_pop
        # Must be efficient
        raise NotImplementedError

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
                with open('checkpoints/%s/%d' % (str(start_dtg), iteration_count), 'w') as f:
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
