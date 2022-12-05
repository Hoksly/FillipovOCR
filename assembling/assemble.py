from Collection import RawImage, Node, NodeType, Point
from string import digits, ascii_lowercase

import math


class MyNode:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None


OPERATORS = ['-', '+', '*']


class Wrapper:
    def __init__(self, node):
        self.node = node
        self.used = False


class Assembler:
    def __init__(self):
        pass

    @staticmethod
    def assembleTop(nodes: list):
        pass

    @staticmethod
    def assembleBottom(nodes: list):
        pass

    @staticmethod
    def _parseNumber(wrappedNodes: list):
        assert wrappedNodes[0].node.value in digits
        wrappedNodes[0].used = True
        headBox, lastBox = wrappedNodes[0].node.box, None

        i = 1
        resValue = wrappedNodes[0].node.value
        while i < len(wrappedNodes) and wrappedNodes[i].node.value in digits and \
            wrappedNodes[i-1].node.inOneLine(wrappedNodes[i].node):

            i += 1
            resValue += wrappedNodes[i].node.value
            wrappedNodes[i].used = True
            lastBox = wrappedNodes[i].node.box

        resBox = (headBox[0], lastBox[1]) if lastBox else headBox

        return Node(NodeType.NUMBER, resValue, resBox)


    @staticmethod
    def _parseFunction(nodes: list):
        pass

    @staticmethod
    def _parseOperator(wrappedNodes: list):
        assert wrappedNodes[0].node.value in OPERATORS
        wrappedNodes[0].used = True
        resVal = wrappedNodes[0].node.value
        if wrappedNodes[0].node.value == '-':
            if wrappedNodes[1].node.value == '-':
                wrappedNodes[1].used = True
                resVal = '='

        return Node(NodeType.OPERATOR, resVal, wrappedNodes[0].node.box)

    @staticmethod
    def _parseLetters(wrappedNodes: list):
        assert wrappedNodes[0].node.value in ascii_lowercase

        if wrappedNodes[0].node.value in ['s', 'c', 'l']:
            return Assembler._parseFunction(wrappedNodes)

        resValue = wrappedNodes[0].node.value
        headBox, lastBox = wrappedNodes[0].node.box, None
        i = 1
        while wrappedNodes[i].node.value in ascii_lowercase and \
                wrappedNodes[i - 1].node.inOneLine(wrappedNodes[i].node):
            i += 1
            resValue += wrappedNodes[i].node.value
            wrappedNodes[i].used = True
            lastBox = wrappedNodes[i].node.box

        resBox = (headBox[0], lastBox[1]) if lastBox else headBox
        return Node(NodeType.VARIABLE, resValue, resBox)

    @staticmethod
    def assemble(rawNodes: list):
        """
        :param nodes: list containing Node objects
        :return: Node
        """
        wrappedNodes = []
        collected = []
        for el in rawNodes:
            wrappedNodes.append(Wrapper(el))
        for i in range(len(wrappedNodes)):
            node = wrappedNodes[i]
            if not node.used:
                print(i, node.node.value)
                if node.node.value in OPERATORS:
                    res = Assembler._parseOperator(wrappedNodes[i:])
                    collected.append(res)

                if node.node.value in digits:
                    res = Assembler._parseNumber(wrappedNodes[i:])
                    collected.append(res)

                if node.node.value in ascii_lowercase:
                    res = Assembler._parseLetters(wrappedNodes[i:])
                    collected.append(res)

        print(len(collected))
        for el in collected:
            print(el)

    @staticmethod
    def _parseEq(nodes: list):
        """

        :param nodes:
        :return:
        """

        pass
