#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QDesktopWidget, QApplication, 
    QGridLayout, QWidget, QPushButton, QGroupBox,
    QVBoxLayout, QFileDialog
)

class HistogramApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        grid = QGridLayout()
        self.setLayout(grid)

        # Input Image Box
        box = QGroupBox('Input Image')
        vbox = QVBoxLayout()
        selectButton = QPushButton('Select Input Image')
        selectButton.clicked.connect(self.selectInputImage)
        vbox.addWidget(selectButton)
        box.setLayout(vbox)
        grid.addWidget(box, 0, 0)

        # Target Image Box
        box = QGroupBox('Target Image')
        vbox = QVBoxLayout()
        selectButton = QPushButton('Select Input Image')
        selectButton.clicked.connect(self.selectTargetImage)
        vbox.addWidget(selectButton)
        box.setLayout(vbox)
        grid.addWidget(box, 0, 1)

        # Result Image Box
        box = QGroupBox('Result Image')
        # vbox = QVBoxLayout()
        # box.setLayout(vbox)
        grid.addWidget(box, 0, 2)

        self.resize(1000, 600)

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