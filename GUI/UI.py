import sys
import os
import sip
import math

from PyQt5.QtWidgets import QStackedLayout, QVBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, QCheckBox, \
    QApplication
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

    def getClassNames(self, filename="GUI/.classes_names.txt"):
        if os.path.isfile(filename):

            with open(filename, 'r') as file:
                data = file.read()
                self.classNames = list(data.split(' '))
        else:  # just creating an empty file
            with open(filename, 'w') as file:
                pass

    def __init__(self):
        super().__init__()
        self.mainStack = QVBoxLayout()

        self.imageLabel = QLabel()
        self.classNames = []

        self.rows_count = 8

        self.initUI()

    def initUI(self):
        self.imageLabel = QLabel()
        self.mainStack = QVBoxLayout()
        grid = QGridLayout()
        self.getClassNames()
        print(self.classNames)

        positions = [(i, j) for i in range(math.ceil(len(self.classNames) / self.rows_count)) for j in
                     range(self.rows_count)]

        for position, name in zip(positions, self.classNames):

            if name == '':
                continue
            button = MyButtion(name, self)

            button.clicked.connect(self.buttonClicked)
            button.setLeftClick(self.buttonClicked)

            grid.addWidget(button, *position)

        self.mainStack.addWidget(self.imageLabel)

        self.mainStack.addLayout(grid)

        self.setLayout(self.mainStack)
        self.setWindowTitle('IDK how to name you')

        self.show()

    def magic(self):
        print("some magic")
        self.imageLabel.setPixmap(QPixmap('../images/img2.png'))
        self.imname = '2.png'

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
