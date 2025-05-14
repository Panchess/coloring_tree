from classes import Node, Edge, Graph

# базовые тесты алгоритма с одной корневой вершиной

# 1 -> 2
node1 = Node(1)
node2 = Node(2)

edge12 = Edge(1, 2)

gr1 = Graph([node1, node2], [edge12])
gr1.final()
assert edge12.color == 1

# 1 -> 2 -> 3
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)

edge12 = Edge(1, 2)
edge23 = Edge(2, 3)
gr2 = Graph([node1, node2, node3], [edge12, edge23])
gr2.final()
assert edge12.color == 1
assert edge23.color == 2

# 2 <- 1 -> 3
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)

edge12 = Edge(1, 2)
edge13 = Edge(1, 3)
gr3 = Graph([node1, node2, node3], [edge12, edge13])
gr3.final()
assert {edge12.color, edge13.color} == {1, 2}

# 2 <- 1 -> 3 -> 4
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)

edge12 = Edge(1, 2)
edge13 = Edge(1, 3)
edge34 = Edge(3, 4)
gr4 = Graph([node1, node2, node3, node4], [edge12, edge13, edge34])
gr4.final()
assert edge12.color == 2
assert edge13.color == 1
assert edge34.color == 2

# 2 <- 1 -> 3 -> 4
#           |
#           V
#           5
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)
node5 = Node(5)

edge12 = Edge(1, 2)
edge13 = Edge(1, 3)
edge34 = Edge(3, 4)
edge35 = Edge(3, 5)
gr5 = Graph(
    [node1, node2, node3, node4, node5],
    [edge12, edge13, edge34, edge35],
)
gr5.final()
assert edge12.color == 2
assert edge13.color == 1
assert {edge34.color, edge35.color} == {2, 3}

