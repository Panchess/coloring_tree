from classes import Node, Edge, Graph

# базовые тесты переборного алгоритма

node1 = Node(1)
node2 = Node(2)
node3 = Node(3)

edge13 = Edge(1, 3)
edge23 = Edge(2, 3)
gr1 = Graph([node1, node2, node3], [edge13, edge23])
gr1.final_pereb()
assert {edge13.best_color, edge23.best_color} == {1, 2}


node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)

edge14 = Edge(1, 4)
edge24 = Edge(2, 4)
edge34 = Edge(3, 4)
gr2 = Graph([node1, node2, node3, node4], [edge14, edge24, edge34])
gr2.final_pereb()
assert {edge14.best_color, edge24.best_color, edge34.best_color} == {1, 2, 3}


node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)

edge13 = Edge(1, 3)
edge23 = Edge(2, 3)
edge34 = Edge(3, 4)
gr3 = Graph([node1, node2, node3, node4], [edge13, edge23, edge34])
gr3.final_pereb()
assert {edge13.best_color, edge23.best_color} == {1, 2}
assert edge34.best_color == 3


node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)
node5 = Node(5)
node6 = Node(6)

edge14 = Edge(1, 3)
edge24 = Edge(2, 3)
edge34 = Edge(3, 4)
edge45 = Edge(4,5)
edge56 = Edge(5, 6)
gr4 = Graph(
    [node1, node2, node3, node4, node5, node6],
    [edge14, edge24, edge34, edge45, edge56],
)
gr4.final_pereb()
assert {edge14.best_color, edge24.best_color, edge34.best_color} == {1, 2, 3}
assert edge45.best_color == 4
assert edge56.best_color == 5

node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)
node5 = Node(5)

edge13 = Edge(1, 3)
edge23 = Edge(2, 3)
edge24 = Edge(2, 4)
edge35 = Edge(3, 5)
gr5 = Graph(
    [node1, node2, node3, node4, node5],
    [edge13, edge23, edge24, edge35],
)
gr5.final_pereb()
assert {edge13.best_color, edge23.best_color} == {1, 2}
assert edge24.best_color == 2
assert edge35.best_color == 3


node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)
node5 = Node(5)
node6 = Node(6)

edge13 = Edge(1, 3)
edge23 = Edge(2, 3)
edge24 = Edge(2, 4)
edge35 = Edge(3, 5)
edge36 = Edge(3, 6)
gr6 = Graph(
    [node1, node2, node3, node4, node5, node6],
    [edge13, edge23, edge24, edge35, edge36],
)
gr6.final_pereb()
assert {edge13.best_color, edge23.best_color} == {1, 2}
assert edge24.best_color == 2
assert {edge35.best_color, edge36.best_color} == {3, 4}

