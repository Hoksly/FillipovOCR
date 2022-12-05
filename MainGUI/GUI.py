import shutil
import sys
import os
import sip
import math
from collections import deque
from parsing.parser import Parser
from assembling.assemble import Assembler
from neuro.recognizer import TypeRecognizer
from PyQt5.QtWidgets import QStackedLayout, QVBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, QCheckBox, \
    QApplication, QMenuBar, QMenu, QMainWindow, QAction, qApp, QFileDialog, QMessageBox, QLineEdit, QInputDialog

from PyQt5.QtGui import QPixmap, QKeyEvent, QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtCore



class AskBinary:
    def __init__(self, message):
        self.msgBox = QMessageBox()
        self.msgBox.setText(message)
        self.msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.msgBox.setDefaultButton(QMessageBox.No)
        self.msgBox.buttonClicked.connect(self.buttonClicked)
        self.result = False

    def buttonClicked(self, button):
        if button.text() == "&Yes":
            self.result = True
        else:
            self.result = False

    def ask(self):
        self.msgBox.exec_()
        return self.result


class MyGrid(QVBoxLayout):
    def __init__(self):
        super(MyGrid, self).__init__()


class MyLabel(QLabel):
    def __init__(self, *args, **kargs):
        super(MyLabel, self).__init__(*args, **kargs)


class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mainStack = QVBoxLayout(self)

        self.imageLabel = MyLabel(self)
        self.imageLabel.setText("No image")
        self.imageLabel.setFont(QFont("Arial", 20, QFont.Bold))
        self.imageLabel.setAlignment(Qt.AlignCenter)

        self.parsedVBox = QVBoxLayout(self)
        self.solvedVBox = QVBoxLayout(self)

        self.currentImage = None
        self.buttonsGrid = QGridLayout(self)

        self.middleGrid = QGridLayout(self)
        self.parsedLabel = QLineEdit(self)
        self.solutionLabel = QLineEdit(self)

        self.parsedLatex = MyLabel(self)
        self.solutionLatex = MyLabel(self)

        self.initUI()

    def openImagesFolder(self):
        self.currentFolder = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        self.getImagesFromFolder()
        if not self.datasetFolder:
            self.askAboutExistingDataset()
        self.setNextImage()

    def openImage(self):
        print("HERE")
        self.currentImage = QFileDialog.getOpenFileName(None, "Select image:", '')[0]
        if self.currentImage:
            self.setImage(self.currentImage)

    def parseImage(self):
        parser = Parser()
        rawImages = parser.parseAndConvert(self.currentImage)
        nodes = []
        recognizer = TypeRecognizer(None)
        for raw in rawImages:
            nodes.append(recognizer.recognize(raw))

        self.parsedLabel.setText(Assembler.assemble(nodes))





    def solveIt(self):
        pass

    def addButtons(self):
        openImageButton = QPushButton("open image", self)
        parseButton = QPushButton('parse', self)
        solveButton = QPushButton('solve', self)

        openImageButton.clicked.connect(self.openImage)
        parseButton.clicked.connect(self.parseImage)
        solveButton.clicked.connect(self.solveIt)

        self.buttonsGrid.addWidget(openImageButton, 0, 0)
        self.buttonsGrid.addWidget(None, 0, 1)
        self.buttonsGrid.addWidget(parseButton, 0, 2)
        self.buttonsGrid.addWidget(solveButton, 0, 3)

    def initUI(self):

        self.setLayout(self.mainStack)

        self.mainStack.addWidget(self.imageLabel)
        self.mainStack.addLayout(self.middleGrid)
        self.mainStack.addLayout(self.buttonsGrid)

        self.middleGrid.addLayout(self.parsedVBox, 0, 0)
        self.middleGrid.addLayout(self.solvedVBox, 0, 1)

        self.parsedVBox.addWidget(self.parsedLabel)
        self.parsedVBox.addWidget(self.parsedLatex)
        self.parsedLatex.setText("parsed LATEX")

        self.solvedVBox.addWidget(self.solutionLabel)
        self.solvedVBox.addWidget(self.solutionLatex)
        self.solutionLatex.setText("solution LATEX")

        self.setWindowTitle('IDK how to name you 2.0')

        self.addButtons()



    def setImage(self, imageLocation):
        if (imageLocation):
            self.imageLabel.setPixmap(QPixmap(imageLocation))
        else:
            self.imageLabel.setText("No image")

    @staticmethod
    def checkOrCreateFolder(folderName):
        if not os.path.exists(folderName):
            os.mkdir(folderName)

    @staticmethod
    def showErrorMessage(message):
        msg = QMessageBox()
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)

        msg.exec_()




class MyAppWrapper(QApplication):
    def __init__(self, destructor_callback=None, *args, **kwargs):
        self.destructor_callback = destructor_callback
        super(MyAppWrapper, self).__init__(*args, **kwargs)

    def __del__(self):
        for widget in self.allWidgets():
            del widget

        if self.destructor_callback:
            self.destructor_callback(self)


class Program:


    def __init__(self, workingFolder='', cacheFileName=".UIcache"):
        pass

    def run(self):

        app = MyAppWrapper(None, sys.argv)
        window = MainWindow()
        window.show()
        app.exec_()



def main():
    p = Program()
    p.run()
    del p


if __name__ == '__main__':
    main()
