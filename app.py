#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cv2
import pdb
import numpy as np
import matplotlib

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt

from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QDesktopWidget, QApplication, 
    QGridLayout, QWidget, QPushButton, QGroupBox,
    QVBoxLayout, QFileDialog, QLabel, QSizePolicy
)

from PyQt5.QtGui import QImage, QPixmap


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

    def cdf(self, data):
        _hist = self.hist(data)
        _cdf = np.zeros(256)
        _sum = 0
        for i in range(256):
            _sum += _hist[i]
            _cdf[i] = _sum
        _cdf /= _cdf[-1]
        return _cdf

    def createLUT(self, cdfInput, cdfTarget):
        LUT = np.zeros(256)
        for i in range(256):
            inputVal = cdfInput[i]
            j = 0
            while (j < 255) and (cdfTarget[j] < inputVal):
                j += 1
            LUT[i] = j
        return LUT

    
class HistogramApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.inputImg = None
        self.targetImg = None
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

    def calculateResultImg(self):
        redChInp = self.inputImg[:,:,0]
        greenChInp = self.inputImg[:,:,1]
        blueChInp = self.inputImg[:,:,2]

        redChTrg = self.targetImg[:,:,0]
        greenChTrg = self.targetImg[:,:,1]
        blueChTrg = self.targetImg[:,:,2]

        redInpCDF = self.targetShowBox.cdf(redChInp)
        greenInpCDF = self.targetShowBox.cdf(greenChInp)
        blueInpCDF = self.targetShowBox.cdf(blueChInp)

        redTrgCDF = self.targetShowBox.cdf(redChTrg)
        greenTrgCDF = self.targetShowBox.cdf(greenChTrg)
        blueTrgCDF = self.targetShowBox.cdf(blueChTrg)

        redLUT = self.targetShowBox.createLUT(redInpCDF, redTrgCDF)
        greenLUT = self.targetShowBox.createLUT(greenInpCDF, greenTrgCDF)
        blueLUT = self.targetShowBox.createLUT(blueInpCDF, blueTrgCDF)

        resultRed = self.execLUT(redChInp, redLUT)
        resultGreen = self.execLUT(greenChInp, greenLUT)
        resultBlue = self.execLUT(blueChInp, blueLUT)

        resultImg = np.dstack((resultRed,resultGreen,resultBlue))
        self.resultShowBox.setImg(resultImg)
        self.resultShowBox.calculateHistogram()


    def execLUT(self, inp, LUT):
        inp = np.array(inp)
        x, y = inp.shape
        for i in range(x):
            for j in range(y):
                inp[i][j] = LUT[inp[i][j]]
        return inp


        
        print('Calculating result image')


if __name__ == '__main__':
    
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 6}

    matplotlib.rc('font', **font)

    app = QApplication(sys.argv)
    ex = HistogramApp()
    sys.exit(app.exec_())