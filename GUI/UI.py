import shutil
import sys
import os
import sip
import math
from collections import deque

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



class MyList:
    def __init__(self, max_items=5):
        self._lst = []
        self._lst2 = deque()
        self._max_items = max_items
        self.current_pos = -1

    def push(self, item):

        self._lst2.append(item)
        if len(self._lst2) > 5:
            self._lst2.popleft()

    def get(self):
        if len(self._lst2) > 0:
            return self._lst2.pop()
        return None

    def __len__(self):
        return len(self._lst)


class MyButton(QPushButton):
    def __init__(self, *args, **kwargs):
        self.onRightClick = None
        self.onLeftClick = None
        self.onMiddleClick = None
        super().__init__(*args, **kwargs)


    def mousePressEvent(self, event):
        '''re-implemented to suppress Right-Clicks from selecting items.'''

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                if self.onRightClick:
                    self.onRightClick(self)
            elif event.button() == QtCore.Qt.LeftButton:
                if self.onLeftClick:
                    self.onLeftClick(self)
                return
            elif event.button() == QtCore.Qt.MiddleButton:

                if self.onMiddleClick:
                    self.onMiddleClick(self)
            else:
                super(MyButton, self).mousePressEvent(event)

    def setLeftClick(self, function):
        self.onLeftClick = function

    def setMiddleClick(self, function):
        self.onMiddleClick = function

    def setRightClick(self, function):
        self.onRightClick = function


def askToUseExistingDirectory():
    msgBox = AskBinary("Such directory already exist in dataset. Use it?")
    return msgBox.ask()


class MainWindow(QWidget):

    def __init__(self, imagesFolder=None, datasetFolder=None, classesNames=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if classesNames is None:
            classesNames = []
        self.currentFolder = imagesFolder
        self.datasetFolder = datasetFolder

        self.buttonsGrid = QGridLayout()
        self.mainStack = QVBoxLayout(self)

        self.imageLabel = MyLabel(self)
        self.imageLabel.setText("No image")
        self.imageLabel.setFont(QFont("Arial", 20, QFont.Bold))
        self.imageLabel.setAlignment(Qt.AlignCenter)

        self.classNames = classesNames

        self.buttonsCount = 0
        self.specialButtons = []

        self.previousImages = MyList()

        self.rows_count = 8
        self.defaultButtonName = "Name Me"

        self.allImages = []
        self.currentImage = None

        self.inputLabelActive = False
        self.inputLabel = None

        if self.currentFolder:
            self.getImagesFromFolder()
            self.setNextImage()

        self.initUI()

    def getCache(self):
        return self.currentFolder, self.datasetFolder, self.classNames

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

    def recreateGrid(self):
        self.mainStack.removeItem(self.buttonsGrid)
        for el in range(self.buttonsGrid.count()):
            if self.buttonsGrid.itemAt(el):
                self.buttonsGrid.itemAt(el).widget().deleteLater()

        del self.buttonsGrid

        self.buttonsGrid = QGridLayout()
        self.mainStack.insertLayout(1, self.buttonsGrid)

        self.buttonsCount = 0
        self.specialButtons = []
        self.loadClassesButtonsIntoGrid()
        self.addOperationButtons(self.buttonsGrid)

    def loadClassesButtonsIntoGrid(self):
        if not self.classNames:
            return

        positions = [(i, j) for i in range(math.ceil(len(self.classNames) / self.rows_count)) for j in
                     range(self.rows_count)]

        for position, name in zip(positions, self.classNames):

            if name == '':
                continue
            button = MyButton(name, self)

            button.setLeftClick(self.buttonLeftClicked)
            button.setRightClick(self.buttonRightClicked)
            button.setMiddleClick(self.buttonMiddleClicked)

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

    def askAboutExistingDataset(self):
        msg = QMessageBox()
        msg.setText("Create new dataset?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        msg.setDefaultButton(QMessageBox.Yes)
        msg.buttonClicked.connect(self.popupClicked)

        msg.exec_()

    def openImagesFolder(self):
        self.currentFolder = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        self.getImagesFromFolder()
        if not self.datasetFolder:
            self.askAboutExistingDataset()
        self.setNextImage()

    def openDataset(self):
        self.datasetFolder = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        if self.datasetFolder and os.path.isdir(self.datasetFolder):
            datasetClasses = os.listdir(self.datasetFolder)
            allClassesAlreadyInDataset = True
            for el in datasetClasses:
                if el not in self.classNames:
                    allClassesAlreadyInDataset = False
                    break
            if not allClassesAlreadyInDataset:
                msg = AskBinary("Found additional classes in dataset. Update?")
                if msg.ask():
                    for el in datasetClasses:
                        if el not in self.classNames:
                            self.classNames.append(el)
                    self.recreateGrid()


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
        fileMenu.addAction('Parsed folder', lambda: self.openImagesFolder())
        fileMenu.addAction('Dataset', lambda: self.openDataset())

        parseMenu = QMenu("Parse", menuBar)
        parseMenu.addAction('Folder', lambda: self.parseFolder())
        parseMenu.addAction('Image', lambda: self.parseImage())

        settingsMenu = QMenu("Settings", menuBar)

        menuBar.addMenu(fileMenu)
        menuBar.addMenu(parseMenu)
        menuBar.addMenu(settingsMenu)

        return menuBar

    def addButton(self, buttonName: str):
        if os.path.isdir(self.datasetFolder + '/' + buttonName):
            if not askToUseExistingDirectory():
                shutil.rmtree(self.datasetFolder + '/' + buttonName)

        if self.buttonsCount > 4 and self.rows_count - (self.buttonsCount - 4) % self.rows_count != self.rows_count:
            y = (math.ceil((self.buttonsCount - 4) / self.rows_count)) - 1
            x = (self.buttonsCount - 4) % self.rows_count


            button = MyButton(buttonName, self)

            button.setLeftClick(self.buttonLeftClicked)
            button.setRightClick(self.buttonRightClicked)
            button.setMiddleClick(self.buttonMiddleClicked)

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

            self.buttonsCount -= len(self.specialButtons) if self.specialButtons else 0

            self.specialButtons.clear()
            # future coordinates at grid
            y = self.buttonsCount // self.rows_count
            x = 0
            # actual button adding
            button = MyButton(buttonName, self)

            button.setLeftClick(self.buttonLeftClicked)
            button.setRightClick(self.buttonRightClicked)
            button.setMiddleClick(self.buttonMiddleClicked)

            self.buttonsGrid.addWidget(button, y, x)
            self.buttonsCount += 1
            # place our special buttons again
            self.addOperationButtons(self.buttonsGrid)
    def addButtonClicked(self, button: MyButton, newButtonName = None):
        # if we have enough place on a grid and no need to move it
        self.addButton(self.defaultButtonName)




    def removeButtonFromGrid(self, buttonName):
        removeButton = True
        if self.defaultButtonName != buttonName:
            filesCount = len(os.listdir(self.datasetFolder + '/' + buttonName)) \
                if self.datasetFolder and os.path.isdir(self.datasetFolder + '/' + buttonName) \
                else 0

            messageBox = AskBinary("Are you sure you want to remove this button. \n Also directory will be removed." +
                                   (" {} File{} will be remove".format(filesCount, "s" if filesCount > 1 else "") if filesCount else ""))
            removeButton = messageBox.ask()

        if not removeButton:
            return

        if self.datasetFolder and os.path.exists(self.datasetFolder + '/' + buttonName):
            shutil.rmtree(self.datasetFolder + '/' + buttonName)

        for i in range(self.buttonsGrid.count()):
            item = self.buttonsGrid.itemAt(i)
            if item:
                if item.widget().text() == buttonName:
                    item.widget().deleteLater()
                    self.buttonsCount -= 1


        self.recreateGrid()

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

        if previous_image:
            if(self.currentImage):
                self.allImages.append(self.currentImage)
            self.currentImage = previous_image
            self.setImage(previous_image)

    def addOperationButtons(self, grid):
        operationButtonsLevel = math.ceil(self.buttonsCount / self.rows_count) + 1
        addButton = QPushButton('add', self)
        backButton = QPushButton('back', self)
        skipButton = QPushButton('skip', self)
        deleteButton = QPushButton('del', self)

        addButton.clicked.connect(self.addButtonClicked)
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
        if not self.allImages and not self.currentImage:
            return False
        if not self.datasetFolder or not os.path.exists(self.datasetFolder):
            msg = QMessageBox()
            msg.setText("Please select dataset folder first")
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec_()
            return False

        if self.allImages and not self.datasetFolder:
            self.createDatasetFolder()

        folderName = self.datasetFolder + '/' + className

        destination = self.moveImageFile(self.currentImage, folderName)

        if destination:
            self.previousImages.push(destination)

        return True

    def buttonLeftClicked(self, btn: MyButton):

        if self.moveImage(btn.text()):
            self.setNextImage()

    def checkNewName(self, newName: str):
        return len(newName) > 0 and newName[0] != '.'

    def changeFolderName(self, previousName, newName):
        if self.datasetFolder and os.path.isdir(self.datasetFolder) and os.path.isdir(
                self.datasetFolder + '/' + previousName):
            os.rename(self.datasetFolder + '/' + previousName, self.datasetFolder + '/' + newName)

    @staticmethod
    def showErrorMessage(message):
        msg = QMessageBox()
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)

        msg.exec_()


    def buttonRightClicked(self, btn: MyButton):
        'Change name of a button'
        newButtonName, okPressed = QInputDialog.getText(
            self, 'Button dialog', 'Enter new button name:')
        if okPressed:

            if self.checkNewName(newButtonName):

                if newButtonName not in self.classNames:
                    if btn.text() == self.defaultButtonName:

                        self.classNames.append(newButtonName)

                    elif btn.text() in self.classNames:
                        self.classNames.remove(btn.text())
                        self.classNames.append(newButtonName)

                    if os.path.isdir(self.datasetFolder + '/' + newButtonName):
                        if not askToUseExistingDirectory():
                            shutil.rmtree(self.datasetFolder + '/' + newButtonName)

                    self.changeFolderName(btn.text(), newButtonName)
                    btn.setText(newButtonName)
                else:
                    self.showErrorMessage("Such class already exist")

            else:
                self.showErrorMessage("Name of class is not correct (can't be hidden)")

    def buttonMiddleClicked(self, btn: MyButton):
        "delete button"

        if btn.text() in self.classNames:
            self.classNames.remove(btn.text())

        self.removeButtonFromGrid(btn.text())

    def keyPressEvent(self, e: QKeyEvent) -> None:

        if e.key() == QtCore.Qt.Key.Key_F1:
            if not self.inputLabelActive:
                self.inputLabelActive = True
                self.inputLabel = QLineEdit(self)
                self.mainStack.addWidget(self.inputLabel)
            else:
                self.inputLabelActive = False
                self.inputLabel = None
                self.mainStack.itemAt(2).widget().deleteLater()
        if e.key() == 16777220 and self.inputLabelActive: # Enter pressed
            labelText = self.inputLabel.text()
            if labelText in self.classNames:

                self.moveImage(labelText)
                self.setNextImage()
            elif labelText != "":
                msgBox = AskBinary("No such class: " + labelText + " Add it?")
                if msgBox.ask():
                    self.addButton(labelText)
                    self.classNames.append(labelText)
                    self.moveImage(labelText)
                    self.setNextImage()


            self.inputLabel.setText("")

        if e.key() == QtCore.Qt.Key.Key_Tab:
            pass



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

    def clearClasses(self):
        self.classesNames = [i for i in self.classesNames if i != '']

    def readCache(self, filename):
        with open(filename, 'r') as file:
            data = file.read()
            lines = data.split('\n')
            folderNames = lines[0].split(' ') if lines else None
            self.datasetFolder = folderNames[0] if folderNames and lines[0] != "None" else None
            self.imagesFolder = folderNames[1] if len(folderNames) > 1 and lines[1] != "None" else None

            self.classesNames = list(lines[1].split(' ')) if lines and len(lines) > 1 and len(lines[1]) > 1 else []

        self.clearClasses()
        self.classesNames.sort()

    def writeCache(self, filename):
        with open(filename, 'w') as file:
            out = (self.datasetFolder if self.datasetFolder else 'None') + ' ' + (
                self.imagesFolder if self.imagesFolder else 'None')
            out += '\n'
            for el in self.classesNames:
                out += el + ' '
            file.write(out)

    def __init__(self, workingFolder='', cacheFileName=".UIcache"):
        self.app = None
        self.window = None

        self.datasetFolder = None
        self.imagesFolder = None
        self.classesNames = []

        self.fullCachePath = workingFolder + '/' + cacheFileName if workingFolder else cacheFileName
        if os.path.exists(self.fullCachePath):
            self.readCache(self.fullCachePath)


    def run(self):

        app = MyAppWrapper(None, sys.argv)
        window = MainWindow(imagesFolder=self.imagesFolder, datasetFolder=self.datasetFolder,
                            classesNames=self.classesNames)
        window.show()
        app.exec_()

        self.imagesFolder, self.datasetFolder, self.classesNames = window.getCache()

        self.writeCache(self.fullCachePath)


def main():
    p = Program()
    p.run()
    del p


if __name__ == '__main__':
    main()
