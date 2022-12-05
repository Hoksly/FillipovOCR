from parsing.parser import Parser
from Collection import RawImage, Node, Point, NodeType
from assembling.assemble import Assembler
import os

if __name__ == '__main__':
    xNode = Node(NodeType.VARIABLE, 'x', (Point(20, 0), Point(20, 20)))
    minNode1 = Node(NodeType.OPERATOR, '-', (Point(22, 11), Point(28, 13)))
    minNode2 = Node(NodeType.OPERATOR, '-', (Point(22, 6), Point(28, 8)))
    resNode = Node(NodeType.NUMBER, '8', (Point(30, 0), Point(40, 23)))


    (Assembler.assemble([xNode, minNode1, minNode2, resNode]))

    