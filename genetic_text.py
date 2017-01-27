from .genetic_algorithm import GeneticAlgorithm
import numpy
# FUTURE Replace numpy with a bit level implemenation


class GeneticText(object):
    def __init__(self):
        self.GA = GeneticAlgorithm()

    def generate_text(self, text, verbose=False):
        self.GA.target = self.to_array(text)

        while True:
            self.GA.step(verbose)

    def to_array(self, text):
        # TODO convert text (str) to a numpy array with dtype uint8
        return []

    def to_text(self, array):
        # TODO convert numpy array of dtype uint8 to str
        return ''

