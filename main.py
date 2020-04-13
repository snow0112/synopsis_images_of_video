from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from cv2 import cv2
import multimediaUI
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget


class MyQtApp(multimediaUI.Ui_MainWindow, QtWidgets.QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Multimedia Project")
        self.import_PB.clicked.connect(self.openFile)
        self.toolButton.clicked.connect(self.openFile)

    def openFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            # self.mediaPlayer.setMedia(
            #         QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.pauseButton.setEnabled(True)
            self.stopButton.setEnabled(True)





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    qt_app = MyQtApp()
    qt_app.show()
    sys.exit(app.exec_())
