import math

from PIL import Image
import numpy as np
import cv2
from Collection import RawImage, Point


def dispaly(image):
    # show the image, provide window name first
    cv2.imshow('image window', image)
    # add wait key. window waits until user presses a key
    cv2.waitKey(0)
    # and finally destroy/close all open windows
    cv2.destroyAllWindows()


class MyQueue:
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

    def __init__(self, targetSizes=(75, 75), binaryThreshold=cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
                 scaleFully=False, scaleFullyRate=0.9, whiteThreshold=249, blackThreshold=0,
                 rescalingInterpolation=cv2.INTER_AREA, pixelsInImageThreshold=20,
                 rescaleOriginalImage=True, rescaleToAtLeast=200, rescaleToAtMaximum=1000):


        self.targetWidth = targetSizes[0]
        self.targetHeight = targetSizes[1]

        self.binaryThreshold = binaryThreshold

        self.scaleFully = scaleFully
        self.scaleFullyRate = scaleFullyRate

        self.whiteThreshold = whiteThreshold
        self.blackThreshold = blackThreshold

        self.rescalingInterpolation = rescalingInterpolation
        self.pixelsInIMageThreshold = pixelsInImageThreshold

        self.rescaleOriginalImage = rescaleOriginalImage
        self.rescaleOriginalMin = rescaleToAtLeast
        self.rescaleOriginalMax = rescaleToAtMaximum

        self.parseMode = 1

    def _imageToBinary(self, image, zeroValueTrash=0, oneValueTrash=253):
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, binary = cv2.threshold(grayImage, self.blackThreshold, self.whiteThreshold, self.binaryThreshold)
        # cv2.imwrite("Test.png", binary)
        return binary

    def _BNF(self, binaryImage):

        Q = MyQueue()
        whitePixels = []


        for i in range(len(binaryImage)):
            for j in range(len(binaryImage[i])):
                if binaryImage[i][j] > self.whiteThreshold-1:
                    Q.put((i, j))
                    binaryImage[i][j] = 0
                    obj = []


                    while not Q.empty():
                        i, j = Q.pop()

                        obj.append((i, j))

                        if i + 1 < len(binaryImage) and binaryImage[i + 1][j] != 0:
                            Q.put((i + 1, j))
                            binaryImage[i + 1][j] = 0

                        if j - 1 > 0 and binaryImage[i][j - 1] != 0:
                            Q.put((i, j - 1))
                            binaryImage[i][j - 1] = 0

                        if i - 1 > 0 and binaryImage[i - 1][j] != 0:
                            Q.put((i - 1, j))
                            binaryImage[i - 1][j] = 0

                        if j + 1 < len(binaryImage[i]) and binaryImage[i][j + 1] != 0:
                            Q.put((i, j + 1))
                            binaryImage[i][j + 1] = 0

                        if self.parseMode == 1:
                            if i + 1 < len(binaryImage) and j+1 < len(binaryImage[i+1]) and binaryImage[i + 1][j+1] != 0:
                                Q.put((i + 1, j+1))
                                binaryImage[i + 1][j+1] = 0
                            if i + 1 < len(binaryImage) and j - 1 > 0 and binaryImage[i + 1][j-1] != 0:
                                Q.put((i + 1, j-1))
                                binaryImage[i + 1][j-1] = 0
                            if i - 1 > 0 and j - 1 > 0 and binaryImage[i - 1][j - 1] != 0:
                                Q.put((i - 1, j - 1))
                                binaryImage[i - 1][j - 1] = 0
                            if i - 1 > 0 and j + 1 < len(binaryImage[i-1]) and binaryImage[i - 1][j + 1] != 0:
                                Q.put((i - 1, j + 1))
                                binaryImage[i - 1][j + 1] = 0

                    whitePixels.append(obj)
        return whitePixels

    def _parseImage(self, image_path: str) -> list:

        image = cv2.imread(image_path)
        if self.rescaleOriginalImage:
            image = self.scaleOriginal(image)

        binary = self._imageToBinary(image)

        whitePixels = self._BNF(binary)

        return whitePixels

    def isScaleable(self, imageShape):
        return True

    def scaleOriginal(self, image: np.ndarray):
        # To be created
        return image

    @staticmethod
    def _getImageAndCenterFromDotes(Dotes, originalImage=None):
        i_mx, j_mx = -1, -1
        i_mn, j_mn = 100500, 100500  # just big numbers

        # finding upper right and lower left corner of image
        for el in Dotes:
            i, j = el

            if i_mx < i:
                i_mx = i
            if j_mx < j:
                j_mx = j
            if j_mn > j:
                j_mn = j
            if i_mn > i:
                i_mn = i

        # updating image center
        imageCenter = (Point(i_mn, j_mn), Point(i_mx, j_mx))

        # finding out size of image
        width, height = i_mx - i_mn + 1, j_mx - j_mn + 1
        image = np.zeros((width, height)) if originalImage is None else np.zeros((width, height, 3))

        # recreating image from dotes
        if originalImage is not None:
            for el in Dotes:
                i, j = el
                image[i - i_mn][j - j_mn] = originalImage[i][j]
        else:
            for el in Dotes:
                i, j = el
                image[i - i_mn][j - j_mn] = 255

        return image, imageCenter

    def scaleParsedImage(self, image: np.ndarray):
        """
        :param image: np.ndarray
        :return: scaledImage np.ndarray
        """
        width, height = image.shape if len(image.shape) == 2 else image.shape[0], image.shape[1]

        newWidth = self.targetWidth if width > self.targetHeight else width
        newHeight = self.targetHeight if height > self.targetHeight else height
        if self.scaleFully and newHeight < self.targetHeight * self.scaleFullyRate and newWidth * self.scaleFullyRate:
            scaleRate = min((self.targetWidth * self.scaleFullyRate / newWidth), (
                    self.targetHeight * self.scaleFullyRate / newHeight))

            newWidth = math.ceil(newWidth * scaleRate)
            newHeight = math.ceil(newHeight * scaleRate)



        scaled = cv2.resize(image, (newHeight, newWidth), interpolation=self.rescalingInterpolation)

        # pasting our scaled image in the middle
        x_add, y_add = (self.targetWidth - newWidth) // 2, (self.targetHeight - newHeight) // 2
        resized = np.zeros((self.targetWidth, self.targetHeight)) if len(image.shape) == 2 else np.zeros((self.targetWidth, self.targetHeight, 3))
        for x in range(newWidth):
            for y in range(newHeight):
                resized[x + x_add][y + y_add] = scaled[x][y]

        return resized

    def parseAndConvert(self, image_name: str) -> list:
        imagesInDotes = self._parseImage(image_name)
        original = 255 - cv2.imread(image_name)

        images = []

        for dotes in imagesInDotes:
            image = self._getImageAndCenterFromDotes(dotes, original)
            images.append([self.scaleParsedImage(image[0]), image[1]])
        rawImages = []
        for image, center in images:
            rawImages.append(RawImage(image, center))

        return rawImages

if __name__ == '__main__':
    parser  = Parser()

    for el in parser.parseAndConvert('/root/Github/FillipovOCR/img2.jpg'):
        print(el)