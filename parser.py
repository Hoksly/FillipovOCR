from PIL import Image
import numpy as np
import cv2 as cv
from Collection import RawImage


def dispaly(image):
    # show the image, provide window name first
    cv.imshow('image window', image)
    # add wait key. window waits until user presses a key
    cv.waitKey(0)
    # and finally destroy/close all open windows
    cv.destroyAllWindows()


class MuQueue:
    def __init__(self):
        self.lst = []

    def put(self, obj):
        self.lst.append(obj)

    def pop(self):
        return self.lst.pop(0)

    def qsize(self):
        return len(self.lst)

    def empty(self):
        return len(self.lst) == 0




class Parser:
    @staticmethod
    def parseImage(image_path: str) -> list:

        image = cv.imread(image_path)

        image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        ret, binary = cv.threshold(image_gray, 0, 253, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)


        objs = []

        Q = MuQueue()

        for i in range(len(binary)):
            for j in range(len(binary[i])):
                if binary[i][j] > 250:
                    Q.put((i, j))
                    binary[i][j] = 0
                    obj = []
                    print(i, j)

                    while not Q.empty():
                        i, j = Q.pop()

                        obj.append((i, j))

                        if i + 1 < len(binary) and binary[i + 1][j] != 0:
                            Q.put((i + 1, j))
                            binary[i + 1][j] = 0

                        if j - 1 > 0 and binary[i][j - 1] != 0:
                            Q.put((i, j - 1))
                            binary[i][j - 1] = 0

                        if i - 1 > 0 and binary[i-1][j] != 0:
                            Q.put((i - 1, j))
                            binary[i - 1][j] = 0

                        if j + 1 < len(binary[i]) and binary[i][j + 1] != 0:
                            Q.put((i, j + 1))
                            binary[i][j + 1] = 0

                    objs.append(obj)
        return objs

    def parseAndConvert(self, image_name :str) -> list:
        images_in_dotes = self.parseImage(image_name)

        raw_images = []
        for lst in images_in_dotes:
            raw_images.append(RawImage(lst))
        return raw_images




