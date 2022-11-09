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
    @staticmethod
    def image_from_dotes(Dotes):
        i_mx, j_mx = -1, -1
        i_mn, j_mn = 100500, 100500

        # finding upper right and lower left corner of image
        for el in Dotes:
            i, j = el

            if (i_mx < i):
                i_mx = i
            if j_mx < j:
                j_mx = j
            if j_mn > j:
                j_mn = j
            if i_mn > i:
                i_mn = i

        # updating image center
        image_center = Point((i_mx + i_mn) // 2, (j_mx + j_mn) // 2)

        # finding out size of image
        width, height = i_mx - i_mn + 1, j_mx - j_mn + 1
        image = np.zeros((width, height))

        # recreating image from dotes
        for el in Dotes:
            i, j = el
            image[i - i_mn][j - j_mn] = 255

        return image, image_center

    @staticmethod
    def scale_to(image: np.ndarray, target_width=75, target_height=75):

        width, height = image.shape

        # to scale each side properly, if image is less than 30x30 it will be pasted
        # in the center of 30x30 black image
        new_width = target_width if width > target_height else width
        new_height = target_height if height > target_height else height

        # scaling our image to the maximum of 30 px in width and height
        scaled = cv2.resize(image, (new_height, new_width), interpolation=cv2.INTER_AREA)

        # pasting our scaled image in the middle of form 30x30
        x_add, y_add = (target_width - new_width) // 2, (target_height - new_height) // 2
        resized = np.zeros((target_width, target_height))
        for x in range(new_width):
            for y in range(new_height):
                resized[x + x_add][y + y_add] = scaled[x][y]

        return resized

    def __init__(self, dotes: np.array) -> None:
        """
        :param dotes: np.array of dotes [(x1, y1) ... (xn, yn)]
        """
        self.Dotes = dotes

        self.not_scaled_image, self.image_center = self.image_from_dotes(self.Dotes)

        self.image = self.scale_to(self.not_scaled_image)

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
