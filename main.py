from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from cv2 import cv2
import multimediaUI
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import imagetool as readrgb
import time

class MyQtApp(multimediaUI.Ui_MainWindow, QtWidgets.QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Multimedia Project")
        #self.import_PB.clicked.connect(self.openFile)
        #self.toolButton.clicked.connect(self.openFile)

        self.folderName = "../../576RGBVideo1/"

        self.play_btn.clicked.connect(self.play)
        self.pause_btn.clicked.connect(self.pause)
        self.stop_btn.clicked.connect(self.stop)
        
        #synopsis = QImage(352*5, 288, QImage.Format_RGB32)
        #pixmap_syn = QtGui.QPixmap("test_synopis.png")
        synopsis = readrgb.readrgbtoQImage("test-MySynopsis.rgb", 352*5, 288)
        pixmap_syn = QPixmap.fromImage(synopsis)
        self.synopsis.setPixmap(pixmap_syn)
        self.synopsis.mousePressEvent = self.getPos
        self.total_length = 880 # synopsis from 0 to 880

        self.frames = []
        for num in range(290, 300):
            fileName = "image-"+str(num).zfill(4)+".rgb"
            #print(fileName)
            video = readrgb.readrgbtoQImage(self.folderName+fileName)
            #pixmap_vdo = QPixmap.fromImage(video)
            self.frames.append( QPixmap.fromImage(video) )
       
    def play(self):
        print("play")
        for num in range(250, 300):
            fileName = "image-"+str(num).zfill(4)+".rgb"
            #print(fileName)
            video = readrgb.readrgbtoQImage(self.folderName+fileName)
            pixmap_vdo = QPixmap.fromImage(video)
            self.video.setPixmap(pixmap_vdo)
            self.video.repaint()
            time.sleep(0.03)
            #print("update")
        #self.video.setPixmap(QtGui.QPixmap("image-0006.jpg"))

    def pause(self):
        print("pause")
        for frame in self.frames:
            self.video.setPixmap(frame)
            self.video.repaint()
            time.sleep(0.03333)  

    def stop(self):
        print("stop")
        video = QImage(352, 288, QImage.Format_RGB32)
        pixmap_vdo = QPixmap.fromImage(video)
        self.video.setPixmap(pixmap_vdo)
        self.video.repaint()

    def getPos(self, event):
        x = event.pos().x()
        print(x)
        video = QtGui.QMovie("test.gif")
        self.video.setMovie(video)
        video.start()
        #print(event.pos().x(), event.pos().y())
        
    #def openFile(self):
    #    fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
    #            QDir.homePath())
    #
    #    if fileName != '':
    #        # self.mediaPlayer.setMedia(
    #        #         QMediaContent(QUrl.fromLocalFile(fileName)))
    #        self.playButton.setEnabled(True)
    #        self.pauseButton.setEnabled(True)
    #        self.stopButton.setEnabled(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    qt_app = MyQtApp()
    qt_app.show()
    sys.exit(app.exec_())
