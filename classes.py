import random
from itertools import permutations
import time
from collections import defaultdict


def take_first(elem):
    return elem[0]

class Node:
    value: int

    def __init__(self, value):
        self.value = value


class Edge:
    incoming: int
    outcoming: int
    color: int | None
    pre_color: int | None
    root_node: set[int | None]
    best_color: int | None
    is_solo: bool | None
    current_color: int | None

    def __init__(self, outcomming, incoming):
        self.incoming = incoming
        self.outcoming = outcomming
        self.color = None
        self.pre_color = None
        self.root_node = set()
        self.best_color = None
        self.is_solo = None
        self.current_color = None

    def color(self, color):
        self.color = color


class Graph:
    nodes: list[Node]
    edges: list[Edge]
    roots: list[int]
    max_color: int
    inc: list[int]

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.edge_color = {}
        self.max_color = 1001

    # все ребра входящие в вершину value
    def incoming_edges(self, value):
        return [edge for edge in self.edges if edge.incoming == value]

    # все выходящие ребра из вершины
    def outcoming_edges(self, value):
        return [edge for edge in self.edges if edge.outcoming == value]

    # все ребра по которым можно дойти из вершины value
    def outcoming_nodes_from_node(self, value):
        answer_values = set()
        new_answer_values = set()
        new_answer_values.add(value)

        while len(new_answer_values) != len(answer_values):
            answer_values = new_answer_values.copy()
            for edge in self.edges:
                if edge.outcoming in answer_values:
                    new_answer_values.add(edge.incoming)

        return [edge for edge in self.edges if edge.outcoming in answer_values]

    # по вершине смотрим не отмечены ли все ребра выходящие из данной вершины
    # и сразу красим все входящие если исходящие отмечены
    def is_pre_color(self, value):
        outcoming_edges = self.outcoming_edges(value)
        pre_color = []
        for edge in outcoming_edges:
            if not edge.pre_color:
                return None
            pre_color.append(edge.pre_color)

        pre_color.sort()
        max_pre_color = 0
        for i in range(len(pre_color)):
            max_pre_color = max(
                max_pre_color,
                pre_color[i] + len(pre_color) - i,
            )

        new_pre_color = max_pre_color + 1
        incoming_edges = self.incoming_edges(value)
        for edge in incoming_edges:
            edge.pre_color = new_pre_color

        return new_pre_color

    # для каждого ребра находим корневую
    def finding_root(self):
        roots = []
        for node in self.nodes:
            if not self.incoming_edges(node.value):
                roots.append(node)
                node.root_node = {node.value}
        self.roots = [r.value for r in roots]

        for root in roots:
            new = self.outcoming_nodes_from_node(root.value)
            for edge in new:
                edge.root_node.add(root.value)

    # находим все не отмеченные в данный момент для корневой root_value
    def find_hanging_not_color(self, root_value):
        edges_root = [
            edge.incoming for edge in self.edges
            if root_value in edge.root_node
        ]

        while not self.is_pre_color(root_value):
            for val in edges_root:
                self.is_pre_color(val)

    # для текущей вершины красим все исходящие ребра
    def color_edges(self, value):
        incoming_edges = self.incoming_edges(value)
        outcoming_edges = self.outcoming_edges(value)
        if not outcoming_edges:
            return
        if incoming_edges:
            max_color = max(edge.color or 0 for edge in incoming_edges)
        else:
            max_color = 0

        edge_pre_color = [(edge.pre_color,edge) for edge in outcoming_edges]
        edge_pre_color.sort(key=take_first, reverse=True)
        index = 1
        for edge in edge_pre_color:
            edge[1].color = max(max_color + index, edge[1].color or 0)
            index += 1
            self.color_edges(edge[1].incoming)
        return


    # красим дерево с корневой вершиной
    def pre_color_tree(self, root_value):
        edges_root = [
            edge for edge in self.edges
            if root_value in edge.root_node
        ]
        root_edges_pre_color = [
            edge.pre_color for edge in edges_root
            if root_value == edge.outcoming
        ]
        root_edges_pre_color.sort()
        max_pre_color = 1
        for i in range(len(root_edges_pre_color)):
            max_pre_color = max(
                max_pre_color,
                root_edges_pre_color[i] + len(root_edges_pre_color) - i,
            )

        self.color_edges(root_value)

    # решаем коализии
    def resolve_coalizion(self):
        problems = 1
        while problems:
            problems = 0
            for node in self.nodes:
                incoming_edges = self.incoming_edges(node.value)
                if len(incoming_edges) < 2:
                    continue
                edge_by_color = {}
                for edge in incoming_edges:
                    if not edge_by_color.get(edge.color):
                        edge_by_color[edge.color] = []
                    edge_by_color[edge.color].append(edge)
                for color, edges_confl in edge_by_color.items():
                    if len(edges_confl) < 2:
                        continue
                    problems += 1
                    change = False
                    for edge_conf in edges_confl:
                        outcoming_edges = self.outcoming_edges(
                            edge_conf.outcoming
                        )
                        color_by_outcoming = {
                            edge.color: edge for edge in outcoming_edges
                            if edge.incoming != edge_conf.incoming
                        }
                        if color_by_outcoming.get(color + 1):
                            self.change_color(
                                edge_conf, color_by_outcoming.get(color + 1)
                            )
                            change = True
                            break
                    if not change:
                        edge_conf = edges_confl[0]
                        edge_conf.color += 1
                    if color == max(edge_by_color.keys()):
                        self.increase(edges_confl[0].incoming)
                    if problems:
                        break
                if problems:
                    break


    # увеличить значение всех ребер от вершины value на 1
    def increase(self, value):
        outcoming_edges = self.outcoming_edges(value)
        if not outcoming_edges:
            return

        for edge in outcoming_edges:
            edge.color += 1
            self.increase(edge.incoming)
        return

    # меняем цвета 2 смежных ребер для решения коализии
    def change_color(self, edge1, edge2):
        edge1.color, edge2.color = edge2.color, edge1.color
        incoming_edges = self.incoming_edges(edge2.incoming)
        color_by_incoming = {
            edge.color: edge for edge in incoming_edges
            if edge.outcoming != edge2.outcoming
        }
        if not color_by_incoming.get(edge2.color):
            return
        edge3 = color_by_incoming[edge2.color]
        outcoming_edges = self.outcoming_edges(edge3.outcoming)
        color_by_outcoming = {
            edge.color: edge for edge in outcoming_edges
            if edge.incoming != edge3.incoming
        }
        if not color_by_outcoming.get(edge3.color + 1):
            edge3.color += 1
            return
        return self.change_color(edge3, color_by_outcoming[edge3.color + 1])


    def final(self):
        start = time.time()
        self.finding_root()
        for r in self.roots:
            self.find_hanging_not_color(r)
        for r in self.roots:
            self.pre_color_tree(r)
        self.resolve_coalizion()
        finish = time.time()
        return finish - start


    # для конкретной вершины перебираем все возможные цвета исходящих ребер
    def pereb(self, pereb_nodes, value):
        incoming_edges = self.incoming_edges(value)
        outcoming_edges = self.outcoming_edges(value)

        max_color = 0
        if incoming_edges:
            max_color = max(edge.color for edge in incoming_edges)

        pere = list(permutations(range(
            max_color + 1, max_color + len(outcoming_edges) + 1
        )))
        for colors in pere:
            for number, color in enumerate(colors):
                outcoming_edges[number].color = color
                self.increase2(outcoming_edges[number].incoming)
            for i, values in enumerate(pereb_nodes):
                if values != value:
                    continue
                if len(pereb_nodes) > i + 1:
                    self.pereb(pereb_nodes, pereb_nodes[i + 1])
                else:
                    res = self.resolve_coalition2()
                    if res:
                        max_color = max(
                            [edge.current_color for edge in self.edges]
                        )
                        if max_color < self.max_color:
                            self.max_color = max_color
                            for edge in self.edges:
                                edge.best_color = edge.current_color

    # решаем коализии для переборного алгоритма
    def resolve_coalition2(self):
        max_color = self.edges[0].color
        for edge in self.edges:
            edge.current_color = edge.color
            if edge.color > max_color:
                max_color = edge.color

        if max_color >= self.max_color:
            return False

        problems = 1
        while problems:
            problems = 0
            for node_value in self.inc:
                incoming_edges = self.incoming_edges(node_value)

                # сторим цвета данных
                edge_by_color = defaultdict(list)
                for edge in incoming_edges:
                    edge_by_color[edge.current_color].append(edge)
                for color, edges_confl in edge_by_color.items():
                    if len(edges_confl) < 2:
                        continue
                    problems += 1
                    if color + 1 >= self.max_color:
                        return False
                    if any(edge for edge in edges_confl if edge.is_solo):
                        [edge for edge in edges_confl if edge.is_solo][0].current_color += 1
                    else:
                        chain = False
                        for edge in edges_confl:
                            outcoming_edges = self.outcoming_edges(edge.outcoming)
                            max_color = max(e.current_color for e in outcoming_edges)
                            if max_color == color:
                                chain = True
                                edge.current_color += 1
                                break
                        if not chain:
                            return False
                    if color == max(edge_by_color.keys()):
                        try:
                            self.increase3(node_value)
                        except ValueError:
                            return False
                    break
                if problems:
                    break
        return True

    # увеличить значение всех однозначных ребер от вершины value
    def increase2(self, value):
        outcoming_edges = self.outcoming_edges(value)
        if not outcoming_edges:
            return

        if len(outcoming_edges) > 1:
            return

        incoming_edges = self.incoming_edges(value)

        color = max([edge.color for edge in incoming_edges])

        for edge in outcoming_edges:
            edge.color = color + 1
            self.increase2(edge.incoming)

    # увеличить текущее значение всех ребер от вершины value
    def increase3(self, value):
        outcoming_edges = self.outcoming_edges(value)
        if not outcoming_edges:
            return True

        for edge in outcoming_edges:
            edge.current_color = edge.current_color + 1
            if edge.current_color >= self.max_color:
                raise ValueError
            self.increase3(edge.incoming)

    # ищем вершины для перебора вариантов
    def find_pereb_nodes(self, value, current_nodes):
        outcoming_edges = self.outcoming_edges(value)
        if not outcoming_edges:
            return current_nodes
        incoming_edges = self.incoming_edges(value)
        if not incoming_edges:
            current_nodes.append(value)
        if not all(ie.color for ie in incoming_edges):
            return current_nodes
        if len(outcoming_edges) > 1 and value not in current_nodes:
            current_nodes.append(value)
        for edge in outcoming_edges:
            edge.color = -1
            self.find_pereb_nodes(edge.incoming, current_nodes)
        return current_nodes

    # составляем список вершин для перебора вариантов
    def create_pereb_nodes(self):
        self.finding_root()
        roots = self.roots
        pereb_nodes = []
        for root in roots:
            new_nodes = self.find_pereb_nodes(root, [])
            for elem in new_nodes:
                pereb_nodes.append(elem)

        return pereb_nodes

    # вершины в которые входят несколько ребер
    def find_inc_nodes(self):
        inc_nodes = []
        for node in self.nodes:
            inc = self.incoming_edges(node.value)
            if len(inc) > 1:
                inc_nodes.append(node.value)
        self.inc = inc_nodes

    # находим ребра однозначно задающиеся от цвета другого ребра
    def find_solo(self):
        solo = []
        for root in self.roots:

            outcoming_edges = self.outcoming_edges(root)
            if len(outcoming_edges) > 1:
                for edge in outcoming_edges:
                    edge.is_solo = False
                continue
            outcoming_edges[0].is_solo = True
            if outcoming_edges:
                solo.append(outcoming_edges[0])

        while solo:
            solo_new = []
            for edge in solo:
                outcoming_edges = self.outcoming_edges(edge)
                if len(outcoming_edges) > 1:
                    edge.is_solo = False
                    continue
                edge.is_solo = True
                if outcoming_edges:
                    solo_new.append(outcoming_edges[0])
            solo = solo_new


    def final_pereb(self):
        start = time.time()
        answer = self.create_pereb_nodes()
        self.find_inc_nodes()
        self.find_solo()
        self.pereb(answer, answer[0])
        finish = time.time()
        return finish - start

    # проверка корректности работы алгоритма на правильную раскраску
    def check(self):
        for node in self.nodes:
            incoming_edges = self.incoming_edges(node.value)
            outcoming_edges = self.outcoming_edges(node.value)
            incoming_edges_val = {
                edge.best_color or edge.color for edge in incoming_edges
            }
            outcoming_edges_val = {
                edge.best_color or edge.color for edge in outcoming_edges
            }

            if len(incoming_edges_val) != len(incoming_edges):
                return node.value
            if len(outcoming_edges_val) != len(outcoming_edges):
                return node.value
            if incoming_edges_val and outcoming_edges_val:
                if min(outcoming_edges_val) <= max(incoming_edges_val):
                    return node.value
        return True


def decode(code_p):
    nodes = set(range(1, len(code_p) + 3))
    while code_p:
        v = min(nodes - set(code_p))
        nodes.remove(v)
        yield code_p.pop(0), v
    yield min(nodes), max(nodes)

def create_tree(n):
    code_p = [random.randint(1, n) for _ in range(1, n - 1)]
    edges = decode(code_p)
    tree = Graph(
        [Node(i) for i in range(1, n + 1)],
        [Edge(min(edge[0], edge[1]), max(edge[0], edge[1])) for edge in edges],
    )
    return tree
    
def create2_equal_trees(n):
    code_p = [random.randint(1, n) for _ in range(1, n - 1)]
    code_p2 = code_p.copy()
    edges = decode(code_p)
    tree1 = Graph(
        [Node(i) for i in range(1, n + 1)],
        [Edge(min(edge[0], edge[1]), max(edge[0], edge[1])) for edge in edges],
    )
    edges = decode(code_p2)
    tree2 = Graph(
        [Node(i) for i in range(1, n + 1)],
        [Edge(min(edge[0], edge[1]), max(edge[0], edge[1])) for edge in edges],
    )
    return tree1, tree2
