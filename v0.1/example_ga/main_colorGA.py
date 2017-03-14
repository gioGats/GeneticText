#!/usr/bin/env python3

from math import sqrt, pow
from random import randint, gauss


class BitChromosome(object):
    def __init__(self, data, tgt):
        self.data = data
        self.score = self.score_chromosome(data, tgt)

    def score_chromosome(self, data, tgt):
        r1, g1, b1 = self.to_rgb(data)
        r2, g2, b2 = self.to_rgb(tgt)
        score = sqrt(sum([pow(r1-r2, 2), pow(g1-g2, 2), pow(b1-b2, 2)]))
        return score

    def to_rgb(self, bit_array):
        r = self.to_int(bit_array[0:8])
        g = self.to_int(bit_array[8:16])
        b = self.to_int(bit_array[16:24])
        return r, g, b

    def to_int(self, bit_array):
        value = 0
        for i in range(len(bit_array)):
            x = len(bit_array) - i - 1
            value += int(bit_array[i]) * pow(2, x)
        return value

    def __lt__(self, other):
        return self.score < other.score


class ColorGA(object):
    def __init__(self, target, pop_size, select_size, mutate_size, new_size, pair_size, num_gen):
        self.target = target
        self.pop_size = pop_size
        self.select_size = select_size
        self.mutate_size = mutate_size
        self.new_size = new_size
        self.pair_size = pair_size
        self.num_gen = num_gen
        self.current_pop = []
        for i in range(pop_size):
            self.current_pop.append(self.new_birth())
        self.current_pop.sort()

    def run(self, num_gen=None):
        if num_gen is None:
            num_gen = self.num_gen

        for i in range(num_gen):
            new_gen = []
            for j in range(self.select_size):
                new_gen.append(self.selection_birth())
            for j in range(self.mutate_size):
                new_gen.append(self.mutation_birth())
            for j in range(self.new_size):
                new_gen.append(self.new_birth())
            for j in range(self.pair_size):
                new_gen.append(self.crossover_birth())
            self.current_pop = new_gen
            self.current_pop.sort(reverse=False)
            best = self.current_pop[0]
            print('After Generation %d the best fit chromosome is %s; distance %d' % (i, best.data, best.score))
            if best.score <= 0:
                print('Perfection attained. Terminating all residual life.')
                return True, i
        return False, best.score

    def crossover_birth(self, cross_point_dist='uniform'):
        if cross_point_dist == 'uniform':
            cross_point = randint(0, 23)
        elif cross_point_dist == 'normal':
            cross_point = gauss(11.5, 11.5)
            cross_point = int(cross_point)
            cross_point = min(cross_point, 23)
            cross_point = max(cross_point, 0)
        mom_index = min(randint(0, len(self.current_pop)-1), randint(0, len(self.current_pop)-1))
        mom = self.current_pop[mom_index]

        dad_index = min(randint(0, len(self.current_pop)-1), randint(0, len(self.current_pop)-1))
        dad = self.current_pop[dad_index]
        data = mom.data[0:cross_point] + dad.data[cross_point:24]

        return BitChromosome(data, self.target)

    def mutation_birth(self, num_mutations=1):
        index = min(randint(0, len(self.current_pop)-1), randint(0, len(self.current_pop)-1))
        select = self.current_pop[index]
        data = select.data
        for i in range(num_mutations):
            to_modify = randint(0, 23)
            char = select.data[to_modify]
            if char == '1':
                new = '0'
            else:
                new = '1'
            l = list(select.data)
            l[to_modify] = new
            data = "".join(l)
        return BitChromosome(data, self.target)

    def selection_birth(self):
        index = min(randint(0, len(self.current_pop)-1), randint(0, len(self.current_pop)-1))
        select = self.current_pop[index]
        return select

    def new_birth(self):
        data = ''
        for i in range(24):
            data += str(randint(0, 1))
        return BitChromosome(data, self.target)

if __name__ == '__main__':
    while True:
        try:
            target_string = str(input('What is your input bit string? '))
            if len(target_string) != 24:
                raise ValueError('Incorrect input length')
            target = BitChromosome(target_string, target_string)
            r, g, b = target.to_rgb(target.data)
            print('FYI, Target color is r=%d g=%d b=%d' % (r, g, b))

            pop_size = int(input('How many chromosomes per population? '))
            select_size = int(input('How many chromosomes undergo selection? '))
            mutate_size = int(input('How many chromosomes undergo mutation? '))
            new_size = int(input('How many new chromosomes per generation? '))
            pair_size = int(input('How many crossover pairs? '))
            num_gen = int(input('How many generations? '))
            if pop_size == (select_size + mutate_size + new_size + pair_size):
                break
            else:
                raise ValueError('Incorrect values')
        except ValueError as e:
            print('Input failure...\n')
            print(e)
    ga = ColorGA(target_string, pop_size, select_size, mutate_size, new_size, pair_size, num_gen)
    ga.run(num_gen)
