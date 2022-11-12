import shutil
import sys
import os
import sip
import math
import queue
import collections

from PyQt5.QtWidgets import QStackedLayout, QVBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, QCheckBox, \
    QApplication, QMenuBar, QMenu, QMainWindow, QAction, qApp, QFileDialog, QMessageBox, QLineEdit, QInputDialog

from PyQt5.QtGui import QPixmap, QKeyEvent, QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class MyGrid(QVBoxLayout):
    def __init__(self):
        super(MyGrid, self).__init__()


class MyLabel(QLabel):
    def __init__(self, *args, **kargs):
        super(MyLabel, self).__init__(*args, **kargs)

    @staticmethod
    def keyboardGrabber() -> 'QWidget':
        print("Grabbing")
        return super(MyLabel).keyboardGrabber()

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        print("I am here")
        super(MyLabel, self).keyPressEvent(ev)


class MyList:
    def __init__(self, max_items=5):
        self._lst = []
        self._max_items = max_items
        self.current_pos = -1

    def push(self, item):
        if self.current_pos > -1:
            self._lst = self._lst[0:self.current_pos]

        self._lst.append(item)
        if len(self._lst) > self._max_items:
            self._lst.pop()
        self.current_pos = len(self._lst) - 1

    def get(self):
        if -1 < self.current_pos < len(self._lst):
            self.current_pos -= 1
            return self._lst[self.current_pos]
        return None

    def __len__(self):
        return len(self._lst)


class MyButton(QPushButton):
    def __init__(self, *args, **kwargs):
        self.onRightClick = None
        self.onLeftClick = None
        super().__init__(*args, **kwargs)

    @staticmethod
    def keyboardGrabber() -> 'QWidget':
        print("grabbing button")
        return super(MyButton).keyboardGrabber()

    def releaseKeyboard(self) -> None:
        print("Relasing keyboard")
        super(MyButton, self).releaseKeyboard()

    def mousePressEvent(self, event):
        '''re-implemented to suppress Right-Clicks from selecting items.'''

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                if self.onRightClick:
                    self.onRightClick(self)
                print("RIGHT")
            elif event.button() == QtCore.Qt.LeftButton:
                if self.onLeftClick:
                    self.onLeftClick(self)
                print("LEFT")
                return
            else:
                super(MyButton, self).mousePressEvent(event)

    def setLeftClick(self, function):
        self.onLeftClick = function

    def setRightClick(self, function):
        self.onRightClick = function


class MainWindow(QWidget):

    def __init__(self, imagesFolder=None, datasetFolder=None, destructionCallback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destructionCallback = destructionCallback
        self.buttonsGrid = QGridLayout()
        self.mainStack = QVBoxLayout(self)

        self.imageLabel = MyLabel(self)
        self.imageLabel.setText("No image")
        self.imageLabel.setFont(QFont("Arial", 20, QFont.Bold))
        self.imageLabel.setAlignment(Qt.AlignCenter)

        self.classNames = []
        self.specialButtons = []
        self.buttonsCount = 0
        self.previousImages = MyList()

        self.rows_count = 8
        self.defaultButtonName = "Name Me"

        self.currentFolder = imagesFolder
        self.datasetFolder = datasetFolder
        self.allImages = []
        self.currentImage = None

        self.inputLabelActive = False
        self.inputLabel = None

        self.initUI()

    def __del__(self):
        print("Destruction")
        if self.destructionCallback:
            self.destructionCallback(self)

    def createDatasetFolder(self, defaultName='dataset'):
        i = 1
        resultedName = defaultName
        while os.path.exists(resultedName):
            resultedName = defaultName + '(' + str(i) + ')'
            i += 1
        os.mkdir(resultedName)
        self.datasetFolder = resultedName

    def moveImageFile(self, imageFile, destinationFolder, replace=False):
        self.checkOrCreateFolder(destinationFolder)
        if imageFile and os.path.exists(imageFile):
            newImageName = 'img' + str(len(os.listdir(destinationFolder)))

            if not replace:
                while os.path.exists(destinationFolder + '/' + newImageName + '.png'):
                    newImageName += '0'

            shutil.move(imageFile, destinationFolder + '/' + newImageName + '.png')
            return destinationFolder + '/' + newImageName + '.png'

    def getClassNamesDefault(self, filename="GUI/.classes_names.txt"):
        if os.path.isfile(filename):

            with open(filename, 'r') as file:
                data = file.read()
                if data == '':  # no data in file
                    return
                self.classNames = list(data.split(' '))
        else:  # just creating an empty file
            with open(filename, 'w') as file:
                pass

    def exportClassNamesDefault(self, filename="GUI/.classes_names.txt"):
        with open(filename, 'w') as file:
            file.write(' '.join(self.classNames))

    def loadClassesButtonsIntoGrid(self):

        self.getClassNamesDefault()

        positions = [(i, j) for i in range(math.ceil(len(self.classNames) / self.rows_count)) for j in
                     range(self.rows_count)]

        for position, name in zip(positions, self.classNames):

            if name == '':
                continue
            button = MyButton(name, self)

            button.setLeftClick(self.buttonLeftClicked)
            button.setRightClick(self.buttonRightClicked)

            self.buttonsGrid.addWidget(button, *position)
        self.buttonsCount += len(self.classNames)

    def getImagesFromFolder(self):
        self.allImages.clear()
        if self.currentFolder:

            for filename in os.listdir(self.currentFolder):
                if not os.path.isdir(filename) and len(filename) > 4 and filename[-4:] == '.png':
                    self.allImages.append(self.currentFolder + '/' + filename)

    def popupClicked(self, message):

        if message.text() == "&Yes":
            self.createDatasetFolder()
        else:
            self.datasetFolder = QFileDialog.getExistingDirectory(None, 'Select a dataset folder:', '',
                                                                  QFileDialog.ShowDirsOnly)

    def askAboutExistinDataset(self):
        msg = QMessageBox()
        msg.setText("Create new dataset?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        msg.setDefaultButton(QMessageBox.Yes)
        msg.buttonClicked.connect(self.popupClicked)

        x = msg.exec_()

    def openFolder(self):
        self.currentFolder = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        self.getImagesFromFolder()
        self.askAboutExistinDataset()
        self.setNextImage()

    def parseFolder(self):
        folderToParse = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)

    def parseImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Image selector", "",
                                                "Image files (*.png);;All files (*) ", options=options)

    def createMenu(self):
        menuBar = QMenuBar(self)

        fileMenu = QMenu('Open', menuBar)
        fileMenu.addAction('Parsed folder', lambda: self.openFolder())
        # openParsedFolder = QMenu("Folder", fileMenu)
        # fileMenu.addMenu(openParsedFolder)

        parseMenu = QMenu("Parse", menuBar)
        parseMenu.addAction('Folder', lambda: self.parseFolder())
        parseMenu.addAction('Image', lambda: self.parseImage())

        settingsMenu = QMenu("Settings", menuBar)

        menuBar.addMenu(fileMenu)
        menuBar.addMenu(parseMenu)
        menuBar.addMenu(settingsMenu)

        return menuBar

    def addButtonToGrid(self, grid):
        # if we ahve enough place on a grid and no need to move it

        if self.buttonsCount > 4 and self.rows_count - (self.buttonsCount - 4) % self.rows_count != self.rows_count:
            y = (math.ceil((self.buttonsCount - 4) / self.rows_count)) - 1
            x = (self.buttonsCount - 4) % self.rows_count

            button = MyButton(self.defaultButtonName, self)

            button.setLeftClick(self.buttonLeftClicked)
            button.setRightClick(self.buttonRightClicked)

            self.buttonsGrid.addWidget(button, y, x)

            self.buttonsCount += 1
        # in case we need to move some items
        else:
            # unfortunately grid does not track actual items count, so we need to do it by ourselves
            # removing our special buttons
            for i in range(self.buttonsGrid.count()):
                item = self.buttonsGrid.itemAt(i)
                if item:
                    if item.widget() in self.specialButtons:
                        item.widget().deleteLater()

            self.buttonsCount -= len(self.specialButtons)
            self.specialButtons.clear()
            # future coordinates at grid
            y = self.buttonsCount // self.rows_count
            x = 0
            # actual button adding
            button = MyButton(self.defaultButtonName, self)

            button.setLeftClick(self.buttonLeftClicked)
            button.setRightClick(self.buttonRightClicked)

            self.buttonsGrid.addWidget(button, y, x)
            self.buttonsCount += 1
            # place our special buttons again
            self.addOperationButtons(self.buttonsGrid)

    def deleteImage(self):
        if self.allImages and len(self.allImages) > 0:
            self.allImages.pop()
        if self.currentImage:
            try:
                os.remove(self.currentImage)
            except Exception as e:
                print(e)
        self.setNextImage()

    def skipImage(self):
        if self.allImages and len(self.allImages) > 0:
            self.allImages.pop()
        self.setNextImage()

    def backToPreviousImage(self):
        previous_image = self.previousImages.get()
        self.currentImage = previous_image
        self.setImage(previous_image)

    def addOperationButtons(self, grid):
        operationButtonsLevel = math.ceil(self.buttonsCount / self.rows_count) + 1
        addButton = QPushButton('add', self)
        backButton = QPushButton('back', self)
        skipButton = QPushButton('skip', self)
        deleteButton = QPushButton('del', self)

        addButton.clicked.connect(self.addButtonToGrid)
        backButton.clicked.connect(self.backToPreviousImage)
        skipButton.clicked.connect(self.skipImage)
        deleteButton.clicked.connect(self.deleteImage)

        grid.addWidget(addButton, operationButtonsLevel, 0)
        grid.addWidget(deleteButton, operationButtonsLevel, self.rows_count - 1)
        grid.addWidget(skipButton, operationButtonsLevel, self.rows_count - 2)
        grid.addWidget(backButton, operationButtonsLevel, self.rows_count - 3)

        self.specialButtons.append(addButton)
        self.specialButtons.append(deleteButton)
        self.specialButtons.append(skipButton)
        self.specialButtons.append(backButton)

        self.buttonsCount += 4

    def initUI(self):

        self.setLayout(self.mainStack)

        self.mainStack.addWidget(self.imageLabel)

        self.loadClassesButtonsIntoGrid()

        self.addOperationButtons(self.buttonsGrid)

        self.mainStack.addLayout(self.buttonsGrid)

        self.setWindowTitle('IDK how to name you')

        self.layout().setMenuBar(self.createMenu())

    def setImage(self, imageLocation):
        if (imageLocation):
            self.imageLabel.setPixmap(QPixmap(imageLocation))
        else:
            self.imageLabel.setText("No image")

    def setNextImage(self):
        if self.allImages and len(self.allImages) > 0:
            self.currentImage = self.allImages.pop()
            self.setImage(self.currentImage)
        else:
            self.currentImage = None
            self.imageLabel.setText("No image")

    @staticmethod
    def checkOrCreateFolder(folderName):
        if not os.path.exists(folderName):
            os.mkdir(folderName)

    def moveImage(self, className):
        if not self.allImages:
            return

        if self.allImages and not self.datasetFolder:
            self.createDatasetFolder()

        folderName = self.datasetFolder + '/' + className

        destination = self.moveImageFile(self.currentImage, folderName)
        if destination:
            self.previousImages.push(destination)

    def buttonLeftClicked(self, btn: MyButton):
        self.moveImage(btn.text())

        self.setNextImage()

    def checkNewName(self, newName: str):
        return len(newName) > 0 and newName[0] != '.'

    def changeFolderName(self, previousName, newName):
        if self.datasetFolder and os.path.isdir(self.datasetFolder) and os.path.isdir(
                self.datasetFolder + '/' + previousName):
            os.rename(self.datasetFolder + '/' + previousName, self.datasetFolder + '/' + newName)

    def buttonRightClicked(self, btn: MyButton):
        'Change name of a button'
        newButtonName, okPressed = QInputDialog.getText(
            self, 'Input Dialog', 'Enter your name:')
        if okPressed:
            if self.checkNewName(newButtonName):
                if btn.text() == self.defaultButtonName:
                    self.classNames.append(newButtonName)
                elif btn.text() in self.classNames:
                    self.classNames.remove(btn.text())
                self.changeFolderName(btn.text(), newButtonName)
                btn.setText(newButtonName)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        print("Main:", e.key())
        if e.key() == QtCore.Qt.Key.Key_F1:
            if not self.inputLabelActive:
                self.inputLabelActive = True
                self.inputLabel = QLineEdit(self)
                self.mainStack.addWidget(self.inputLabel)
            else:
                self.inputLabelActive = False
                self.inputLabel = None
                self.mainStack.itemAt(2).widget().deleteLater()
        if e.key() == 16777220:
            print("Enter pressed")

        if e.key() == QtCore.Qt.Key.Key_Tab:
            print('here')


def saveCache(obj):
    print('dest')


class MyAppWrapper(QApplication):
    def __init__(self, destructor_callback=None, *args, **kwargs):
        self.destructor_callback = destructor_callback
        super(MyAppWrapper, self).__init__(*args, **kwargs)

    def __del__(self):
        
        if self.destructor_callback:
            self.destructor_callback(self)


class Program:

    def readCache(self, filename):
        with open(filename, 'r') as file:
            self.datasetFolder = file.readline()
            self.imagesFolder = file.readline()

    def writeCache(self, filename):
        with open(filename, 'w') as file:
            file.write(self.datasetFolder + '\n')
            file.write(self.imagesFolder + '\n')

    def __init__(self, workingFolder=''):
        self.datasetFolder = None
        self.imagesFolder = None
        if os.path.exists(workingFolder + '.UIcache'):
            self.readCache(workingFolder + '.UIcache')

    def run(self):

        app = MyAppWrapper(None, sys.argv)
        self.window = MainWindow(imagesFolder=self.imagesFolder, datasetFolder=self.datasetFolder,
                                 destructionCallback=saveCache)
        self.window.show()
        app.exec_()


if __name__ == '__main__':
    ''' '''
    p = Program()
    p.run()
