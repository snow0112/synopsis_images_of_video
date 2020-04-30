# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'multimediaUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(923, 524)
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.video = QtWidgets.QLabel(self.frame)
        self.video.setGeometry(QtCore.QRect(9, 5, 881, 311))
        self.video.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.video.setText("")
        self.video.setScaledContents(False)
        self.video.setAlignment(QtCore.Qt.AlignCenter)
        self.video.setWordWrap(False)
        self.video.setObjectName("video")
        self.synopsis = QtWidgets.QLabel(self.frame)
        self.synopsis.setGeometry(QtCore.QRect(10, 380, 881, 111))
        self.synopsis.setMouseTracking(True)
        self.synopsis.setFrameShape(QtWidgets.QFrame.Box)
        self.synopsis.setText("")
        self.synopsis.setScaledContents(True)
        self.synopsis.setAlignment(QtCore.Qt.AlignCenter)
        self.synopsis.setObjectName("synopsis")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(10, 320, 871, 51))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 0, 821, 44))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.play_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.play_btn.setObjectName("play_btn")
        self.horizontalLayout.addWidget(self.play_btn)
        self.pause_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pause_btn.setObjectName("pause_btn")
        self.horizontalLayout.addWidget(self.pause_btn)
        self.stop_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.stop_btn.setObjectName("stop_btn")
        self.horizontalLayout.addWidget(self.stop_btn)
        self.sound = QtWidgets.QWidget(self.frame_2)
        self.sound.setGeometry(QtCore.QRect(859, 10, 111, 21))
        self.sound.setObjectName("sound")
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.play_btn.setText(_translate("MainWindow", "play"))
        self.pause_btn.setText(_translate("MainWindow", "pause"))
        self.stop_btn.setText(_translate("MainWindow", "stop"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
