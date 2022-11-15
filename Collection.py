from enum import Enum
import numpy as np
import cv2


class NodeType(Enum):
    VARIABLE = 1
    FUNCTION = 2
    OPERATOR = 3
    NUMBER = 4


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

    def __init__(self, image: np.ndarray, center:Point) -> None:

        self.image = image
        self.center = center

    def save(self, path):
        cv2.imwrite(path, self.image)

    def show(self, name):
        cv2.imshow(name, self.image)


class Node:
    def __init__(self, node_type: NodeType, value: str, center: Point):
        self.type = node_type
        self.value = value
        self.center = center

    def __str__(self):
        return str(self.value) + " " + str(self.center) + ", "
