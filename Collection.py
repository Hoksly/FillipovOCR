from enum import Enum
import numpy as np
import cv2
import math

class NodeType(Enum):
    VARIABLE = 1
    OPERATOR = 2
    NUMBER = 3
    FUNCTION = 4


class FunctionType(Enum):
    SIN = 1
    COS = 2
    LN = 3


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + " " + str(self.y)


class RawImage:

    def __init__(self, image: np.ndarray, center: Point) -> None:
        self.image = image
        self.center = center

    def save(self, path):
        cv2.imwrite(path, self.image)

    def show(self, name):
        cv2.imshow(name, self.image)


class Node:
    def __init__(self, nodeType: NodeType, value: str, box: (Point, Point) = (Point(0, 0), Point(0, 0))):
        self.type = nodeType
        self.value = value
        self.center = Point((box[0].x + box[1].x)/2, (box[0].y + box[1].y)/2)
        self.box = box

    def __str__(self):
        return str(self.value) + " " + str(self.center) + ", "

    def inOneLine(self, another):
        angle = math.atan((another.center.y - self.center.y) / (another.center.x - self.center.x)) / math.pi * 180
        if -15 < angle < 15:
            return True # just for now

        return False
