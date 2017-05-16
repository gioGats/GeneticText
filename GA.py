from ga_utils import *


class Chromosome(object):
    # ISSUE Inefficient approach; probably delete this whole class
    def __init__(self, length, data=None):
        if data is None:
            self._data = create_random(length, bits=True)
        else:
            self._data = data

        self._score = -1.0

    @property
    def data(self):
        return self._data

    @property
    def score(self):
        if self._score >= 0.0:
            return self._score
        else:
            raise ValueError('Chromosome not scored')

    def evaluate(self, target):
        self._score = score_sequence(self._data, target)

    def __repr__(self):
        return self.score, self.data

    def __lt__(self, other):
        return self.score < other.score


class GeneticAlgorithm(object):
    def __init__(self, pop_size, generations):
        self._pop_size = pop_size
        self._generations = generations

        # Initially undefined attributes
        self._target_text = None
        self._target = None
        self._chromosome_length = None
        self._generate_functions = None
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

    def run(self, verbosity=1):
        if None in [self._target_text, self._target, self._generate_functions, self._current_pop, self._next_pop]:
            raise AttributeError('Initialization attributes must be defined before running genetic algorithm.')
        # FUTURE Actual GA implementation
