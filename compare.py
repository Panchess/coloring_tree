from classes import create2_equal_trees
from collections import defaultdict
import argparse


def main(n, k):
    equal = 0
    not_equal = 0
    raz = defaultdict(int)
    correct = 0
    time1 = 0
    time2 = 0
    mrpe = 0
    sum1 = 0
    sum2 = 0
    for i in range(n):
        tree, tree2 = create2_equal_trees(k)
        time1 += tree.final()
        time2 += tree2.final_pereb()
        max_color = max(edge.color for edge in tree.edges)
        sum1 += max_color
        max_color2 = max(edge.best_color for edge in tree2.edges)
        sum2 += max_color2

        mrpe += abs(max_color2 - max_color) / max_color2
        if max_color == max_color2:
            equal += 1
        else:
            not_equal += 1
            raz[max_color - max_color2] += 1

        if tree.check() and tree2.check():
            correct += 1


    print('Максимальные цвета в раскрасках совпадают в', equal, 'случаев')
    print('Расскраски не совпадают', not_equal)
    print('На сколько не совпадают раскраски', raz)
    print('В скольки случаях раскраски оказались правильными', correct)
    print('Среднее время работы полиномиального алгоритма', time1 / n)
    print('Среднее время работы алгоритма перебора', time2 / n)
    print('метрика mrpe', mrpe / n)
    print('Относительная погрешность алгоритма', abs(sum2 - sum1) / sum2)


parser = argparse.ArgumentParser()
parser.add_argument('-n', required=True, type=int, help='количество проходов в цикле')
parser.add_argument('-k', required=True, type=int, help='количество вершин в дереве')
args = parser.parse_args()

if __name__ == "__main__":
    args = parser.parse_args()
    n = args.n
    k = args.k
    main(n, k)
