from ga_utils import *

from time import time
from datetime import datetime
import random
import string


class RandomGuesser(object):
    def __init__(self):
        # Initially undefined attributes
        self._target_text = None
        self._target = None
        self._chromosome_length = None
        self._best_guess = None
        self._best_score = None

    def set_target(self, target_text):
        """
        :param target_text: str
        """
        self._target_text = target_text
        self._target = str_to_bin(target_text)
        self._chromosome_length = len(self._target)

    @property
    def best_candidate(self):
        return self._best_guess

    @property
    def best_candidate_score(self):
        return self._best_score

    def run(self, verbosity=1, max_iterations=float('inf'), max_time=float('inf')):
        # TODO Finish this function
        if None in [self._target_text, self._target]:
            raise AttributeError('Initialization attributes must be defined before running genetic algorithm.')

        # Init of loop tracking variables
        iteration_count = 0
        start_time = time()
        start_dtg = str(datetime.now()).replace(' ', '_')

        while True:
            guess = create_random(self._chromosome_length, bits=True)
            this_score = score_sequence(guess, self._target)

            if this_score > self._best_score:
                self._best_guess = guess
                self._best_score = this_score

            # REPORTING
            # TODO Reporting

            # TERMINATION
            if iteration_count > max_iterations:  # Max iterations
                break
            elif self._best_score == 1.0:  # Perfection
                break
            elif time() - start_time > max_time:  # Time
                break
            else:
                iteration_count += 1