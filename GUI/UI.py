import sys
import os
import sip
import math
import queue

from PyQt5.QtWidgets import QStackedLayout, QVBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, QCheckBox, \
    QApplication, QMenuBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore


class MyQImage:
    def __init__(self, path_to_image):
        if os.path.isfile(path_to_image):
            self.path = path_to_image
            self.qImage = QPixmap(self.path)
        else:
            raise ValueError("Image does not exist: " + path_to_image)


class MyButtion(QPushButton):
    def __init__(self, *args, **kwargs):
        self.onRightClick = None
        self.onLeftClick = None
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        '''re-implemented to suppress Right-Clicks from selecting items.'''

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                if self.onRightClick:
                    self.onLeftClick(self)
                print("RIGHT")
            elif event.button() == QtCore.Qt.LeftButton:
                if self.onLeftClick:
                    self.onLeftClick(self)
                print("LEFT")
                return
            else:
                super(MyButtion, self).mousePressEvent(event)

    def setLeftClick(self, function):
        self.onLeftClick = function

    def setRightClick(self, function):
        self.onRightClick = function


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.mainStack = QVBoxLayout()
        self.imageLabel = QLabel()

        self.classNames = []
        self.imageQueue = queue.Queue()

        self.rows_count = 8

        self.initUI()

    def getClassNamesDefault(self, filename="GUI/.classes_names.txt"):
        if os.path.isfile(filename):

            with open(filename, 'r') as file:
                data = file.read()
                self.classNames = list(data.split(' '))
        else:  # just creating an empty file
            with open(filename, 'w') as file:
                pass

    def exoprtClassNamesDefault(self, filename="GUI/.classes_names.txt"):
        with open(filename, 'w') as file:
            file.write(' '.join(self.classNames))

    def loadClassesButtonsIntoGrid(self):
        grid = QGridLayout()
        self.getClassNamesDefault()

        positions = [(i, j) for i in range(math.ceil(len(self.classNames) / self.rows_count)) for j in
                     range(self.rows_count)]

        for position, name in zip(positions, self.classNames):

            if name == '':
                continue
            button = MyButtion(name, self)

            button.clicked.connect(self.buttonClicked)
            button.setLeftClick(self.buttonClicked)

            grid.addWidget(button, *position)

        return grid

    def _addMenu(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

    def addButtonToGrid(self, grid):
        pass

    def deleteImage(self):
        pass

    def skipImage(self):
        pass

    def backToPriviousImage(self):
        pass

    def addOperationButtons(self, grid):
        operationButtonsLevel = math.ceil(len(self.classNames) / self.rows_count) + 1
        addButton = QPushButton('add', self)
        backButton = QPushButton('back', self)
        skipButton = QPushButton('skip', self)
        deleteButton = QPushButton('del', self)

        addButton.clicked.connect(self.addButtonToGrid)
        backButton.clicked.connect(self.backToPriviousImage)
        skipButton.clicked.connect(self.skipImage)
        deleteButton.clicked.connect(self.deleteImage)

        grid.addWidget(addButton, operationButtonsLevel, 0)
        grid.addWidget(deleteButton, operationButtonsLevel, self.rows_count - 1)
        grid.addWidget(skipButton, operationButtonsLevel, self.rows_count - 2)
        grid.addWidget(backButton, operationButtonsLevel, self.rows_count - 3)

    def initUI(self):
        self.imageLabel = QLabel()
        self.mainStack = QVBoxLayout()

        self.mainStack.addWidget(self.imageLabel)

        grid = self.loadClassesButtonsIntoGrid()

        self.addOperationButtons(grid)

        self.mainStack.addLayout(grid)

        self.setLayout(self.mainStack)
        self.setWindowTitle('IDK how to name you')

        self.show()

    def buttonClicked(self, btn):

        print(btn.text())
        self.mainStack.itemAt(0).widget().deleteLater()
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap("../images/img4.png"))

        self.mainStack.insertWidget(0, self.imageLabel)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
