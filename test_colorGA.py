from main import ColorGA, BitChromosome
from random import randint


def random_string():
    data = ''
    for i in range(24):
        data += str(randint(0, 1))
    return data

if __name__ == '__main__':
    f = open('test_results.txt', 'w')

    trial_settings = [[50, 10, 10, 10, 20],
                      [25, 5, 5, 5, 10],
                      [25, 5, 5, 10, 5],
                      [25, 5, 10, 5, 5],
                      [25, 10, 5, 5, 5]]
    for t in trial_settings:
        scores = []
        remainders = []
        for j in range(25):
            target_string = random_string()
            target = BitChromosome(target_string, target_string)
            r, g, b = target.to_rgb(target.data)
            # print('FYI, Target color is r=%d g=%d b=%d' % (r, g, b))

            pop_size = t[0]
            select_size = t[1]
            mutate_size = t[2]
            new_size = t[3]
            pair_size = t[4]
            num_gen = 500

            ga = ColorGA(target_string, pop_size, select_size, mutate_size, new_size, pair_size, num_gen)
            win, val = ga.run(num_gen)

            if win:
                print('Iteration %d, terminated %d' % (j, val))
                scores.append(val)
            else:
                print('Iteration %d, best distance %d' % (j, val))
                remainders.append(val)
        f.write('Trial Settings   | %d, %d, %d, %d, %d\n' % (t[0], t[1], t[2], t[3], t[4]))
        f.write("Iter to complete | Num: %d; Average: %d; Max: %d\n" %
                (len(scores), (sum(scores)/len(scores)), max(scores)))
        f.write("Dist remaining   | Num: %d; Average: %d; Max: %d\n\n" %
                (len(remainders), (sum(remainders)/len(remainders)), max(remainders)))
    f.close()