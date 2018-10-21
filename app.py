#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QDesktopWidget, QApplication, 
    QGridLayout, QWidget, QPushButton, QGroupBox,
    QVBoxLayout, QFileDialog
)

class ImageSelectUI:

    def __init__(self, app, imgType):
        self.app = app
        self.imgType = imgType
        self.box = QGroupBox(f'Select {imgType} Image')
        self.initUI(imgType)

    def initUI(self, imgType):
        layout = QVBoxLayout()
        selectButton = QPushButton(f'Select {imgType} Image')
        selectButton.clicked.connect(self.selectImage)
        layout.addWidget(selectButton)
        self.box.setLayout(layout)
    
    def selectImage(self, type):
        imgName, _ = QFileDialog.getOpenFileName(
            self.app,
            f'Select {type} Image',
            '~',
            'Image Files (*.png *.jpg *.bmp)'
        )
        self.img = cv2.imread(imgName, cv2.IMREAD_ANYCOLOR)
        self.app.imgSelected(self.img, self.imgType)
    

class ImageShowUI:
    def __init__(self, app, imgType):
        self.app = app
        self.imgType = imgType
        self.box = QGroupBox(f'{imgType} Image')
        self.grid = QGridLayout()
        self.box.setLayout(self.grid)
        self.img = None
    
    def setImg(self, img):
        self.img = img
        qImg = QImage(
            self.img.data,
            self.img.shape[1], # Width
            self.img.shape[0], # Height
            self.img.shape[1] * 3, # Width * 3 : bytesperline
            QImage.Format_RGB888
        )
        imgCanvas = QLabel()
        imgCanvas.setAlignment(QtCore.Qt.AlignCenter)
        origPixMap = QPixmap(qImg)
        pixMap = origPixMap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        imgCanvas.setPixmap(pixMap)
        self.grid.addWidget(imgCanvas, 0, 0, 1, 1)

    def calculateHistogram(self):
        redCh = self.img[:,:,0]
        greenCh = self.img[:,:,1]
        blueCh = self.img[:,:,2]

        xs = np.arange(256)

        redCanvas = FigureCanvas(Figure(figsize=(1, 0.8)))
        redAx = redCanvas.figure.subplots()
        redAx.bar(xs, self.hist(redCh), color='red')

        greenCanvas = FigureCanvas(Figure(figsize=(1, 0.8)))
        greenAx = greenCanvas.figure.subplots()
        greenAx.bar(xs, self.hist(greenCh), color='green')

        blueCanvas = FigureCanvas(Figure(figsize=(1, 0.8)))
        blueAx = blueCanvas.figure.subplots()
        blueAx.bar(xs, self.hist(blueCh), color='blue')

        self.grid.addWidget(redCanvas, 2, 0, 1, 1)
        self.grid.addWidget(greenCanvas, 3, 0, 1, 1)
        self.grid.addWidget(blueCanvas, 4, 0, 1, 1)

    def hist(self, data):
        _hist = np.zeros(256)
        h, w = data.shape
        for i in range(h):
            for j in range(w):
                _hist[data[i][j]] += 1
        return _hist
class HistogramApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Input Image Box
        self.inputSelectBox = ImageSelectUI(self, 'Input')
        self.inputShowBox = ImageShowUI(self, 'Input')
        self.inputShowBox.box.hide()

        # Target Image Box
        self.targetSelectBox = ImageSelectUI(self, 'Target')
        self.targetShowBox = ImageShowUI(self, 'Target')
        self.targetShowBox.box.hide()

        # Result Image Box
        self.resultShowBox = ImageShowUI(self, 'Result')

        #Grid System
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.inputSelectBox.box, 0, 0)
        self.grid.addWidget(self.inputShowBox.box, 0, 0)
        self.grid.addWidget(self.targetSelectBox.box, 0, 1)
        self.grid.addWidget(self.targetShowBox.box, 0, 1)
        self.grid.addWidget(self.resultShowBox.box, 0, 2)

        self.resize(1100, 800)

        windowCenter  = QDesktopWidget().availableGeometry().center()
        frameGeometry = self.frameGeometry()
        frameGeometry.moveCenter(windowCenter)
        self.move(frameGeometry.topLeft())
        self.setWindowTitle('Histogram Matcher')
        self.show()

    def imgSelected(self, img, imgType):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if imgType == 'Input':
            self.inputImg = img
            self.inputShowBox.setImg(img)
            self.inputShowBox.calculateHistogram()
            self.inputSelectBox.box.hide()
            self.inputShowBox.box.show()
        elif imgType == 'Target':
            self.targetImg = img
            self.targetShowBox.setImg(img)
            self.targetShowBox.calculateHistogram()
            self.targetSelectBox.box.hide()
            self.targetShowBox.box.show()

        if (self.inputImg is not None) and (self.targetImg is not None):
            self.calculateResultImg()
    def selectTargetImage(self):
    def calculateResultImg(self):




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HistogramApp()
    sys.exit(app.exec_())