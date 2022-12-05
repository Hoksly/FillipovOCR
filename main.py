from parsing.parser import Parser
from Collection import RawImage, Node, Point, NodeType
from assembling.assemble import Assembler
import os

"""
dNode = Node(NodeType.VARIABLE, 'd', (Point(-15, 0), Point(-3, 20)))
    xNode = Node(NodeType.VARIABLE, 'x', (Point(0, 0), Point(20, 20)))
    minNode1 = Node(NodeType.OPERATOR, '-', (Point(22, 11), Point(28, 13)))
    minNode2 = Node(NodeType.OPERATOR, '-', (Point(22, 6), Point(28, 8)))
    resNode = Node(NodeType.NUMBER, '8', (Point(30, 0), Point(40, 23)))
    resNode1 = Node(NodeType.NUMBER, '3', (Point(42, 0), Point(50, 23)))
    resNode2 = Node(NodeType.NUMBER, '2', (Point(52, 0), Point(60, 23)))

    (Assembler.assemble([dNode, xNode, minNode1, minNode2, resNode, resNode1, resNode2]))


"""

if __name__ == '__main__':
    Node1 = Node(NodeType.VARIABLE, 'y', (Point(0, 0), Point(20, 20)))
    Node2 = Node(NodeType.VARIABLE, "'", (Point(22, 18), Point(24, 25)))
    Node3 = Node(NodeType.VARIABLE, '-', (Point(28, 12), Point(40, 14)))
    Node4 = Node(NodeType.VARIABLE, '-', (Point(27, 6), Point(41, 8)))
    Node5 = Node(NodeType.VARIABLE, 'x', (Point(45, 0), Point(60, 18)))
    Node5n = Node(NodeType.VARIABLE, '-', (Point(47, 10), Point(58, 12)))
    Node6 = Node(NodeType.VARIABLE, 'e', (Point(60, 0), Point(78, 18)))
    Node7 = Node(NodeType.VARIABLE, 'y', (Point(80, 15), Point(85, 19)))

    print(Assembler.assemble([Node1, Node2, Node3, Node4, Node5, Node5n, Node6, Node7]))

