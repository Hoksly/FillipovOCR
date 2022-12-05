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
                wrappedNodes[i - 1].node.inOneLine(wrappedNodes[i].node):
            resValue += wrappedNodes[i].node.value
            wrappedNodes[i].used = True
            lastBox = wrappedNodes[i].node.box
            i += 1

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
        while len(wrappedNodes) > i and wrappedNodes[i].node.value in ascii_lowercase and \
                wrappedNodes[i - 1].node.inOneLine(wrappedNodes[i].node):
            resValue += wrappedNodes[i].node.value
            wrappedNodes[i].used = True
            lastBox = wrappedNodes[i].node.box
            i += 1

        resBox = (headBox[0], lastBox[1]) if lastBox else headBox
        return Node(NodeType.VARIABLE, resValue, resBox)

    @staticmethod
    def _preAssemble(rawNodes: list):
        wrappedNodes = []
        collected = []
        for el in rawNodes:
            wrappedNodes.append(Wrapper(el))

        for i in range(len(wrappedNodes)):
            node = wrappedNodes[i]
            if not node.used:

                if node.node.value in OPERATORS:
                    res = Assembler._parseOperator(wrappedNodes[i:])
                    collected.append(res)

                if node.node.value in digits:
                    res = Assembler._parseNumber(wrappedNodes[i:])
                    collected.append(res)

                if node.node.value in ascii_lowercase:
                    res = Assembler._parseLetters(wrappedNodes[i:])
                    collected.append(res)

        return collected

    @staticmethod
    def _lineAssembly(nodes):
        if not nodes:
            return ""
        if len(nodes) == 1:
            return nodes[0].value

        resString = nodes[0].value
        prevNode = nodes[0]
        for i in range(1, len(nodes)):
            curNode = nodes[i]
            angle = math.atan(
                (curNode.center.y - prevNode.center.y) / (curNode.center.x - prevNode.center.x)) / math.pi * 30
            if -20 < angle < 20 or prevNode.distanceTo(curNode) > prevNode.diagonalSize():
                continue
            resString += " " + curNode.value
            prevNode = curNode
        return resString
    @staticmethod
    def _countAngle(a: Point, b: Point):
        yDiff = a.y - b.y
        xDiff = a.x - b.x
        if xDiff != 0:
            return math.atan(yDiff/xDiff) / math.pi * 180
        return 0

    @staticmethod
    def _finalAssembly(nodes: list):
        if not nodes:
            return ""
        if len(nodes) == 1:
            return nodes[0].value

        resString = nodes[0].value
        prevNode = nodes[0]

        level = 0
        for i in range(1, len(nodes)):
            skip = False
            curNode = nodes[i]
            angle = Assembler._countAngle(prevNode.center, curNode.center)
            print(curNode.value, angle)

            if angle > 30 and curNode.value == "'":  # going up
                while i < len(nodes):
                    curNode = nodes[i]
                    i += 1
                    resString += "'"
                continue

            elif angle > 30:
                level += 1
                resString += '^('
                resString += curNode.value
                prevNode = curNode
                continue

            elif angle < -30:
                level -= 1
                if level < 0:
                    print("Unexpected behaviour")
                resString += ')'
                resString += curNode.value
                prevNode = curNode
                continue
            resString += curNode.value
            prevNode = curNode
        for i in range(level):
            resString += ")"

        return resString




    @staticmethod
    def assemble(rawNodes: list):
        """
        :param rawNodes: list containing Node objects
        :return: Node
        """
        preAssembled = Assembler._preAssemble(rawNodes)
        return Assembler._finalAssembly(preAssembled)
