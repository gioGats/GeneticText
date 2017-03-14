from .genetic_algorithm import GeneticAlgorithm
import pickle


class GeneticText(object):
    def __init__(self):
        self.GA = GeneticAlgorithm()
        self.play_dict = {}

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

    def save(self, play):
        f = open('play_array/%s.npy' % play)
        pickle.dump(self.play_dict[play], f)
        f.close()

    def load(self, play):
        f = open('play_array/%s.npy' % play)
        npy = pickle.load(f)
        f.close()
        self.play_dict[play] = npy

    def load_all(self):
        # TODO For every file in play array:
        #   -parce its filename for the play_name
        #   -self.load(play_name)
        raise NotImplementedError

