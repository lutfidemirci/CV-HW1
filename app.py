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
        
    def selectInputImage(self):
        print('select Input Image')
        
    def selectTargetImage(self):
        print('select Target Image')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HistogramApp()
    sys.exit(app.exec_())