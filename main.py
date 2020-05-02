from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from cv2 import cv2
import multimediaUI
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import imagetool as readrgb
import time
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

import traceback, sys

class Img_Thread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, fn):
        QThread.__init__(self)
        self.fn = fn
        self.n = 0
        self.kill = 0

    def run(self):
        for i in range(self.n):
            if self.kill == 1:
                break
            self.fn()
            time.sleep(0.03)
        self.signal.emit("finished")

        
        
        

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
        synopsis = readrgb.readrgbtoQImage("test-MySynopsis.rgb", 352*15, 288)
        pixmap_syn = QPixmap.fromImage(synopsis)
        #pixmap_syn.scaledToHeight(100)
        self.synopsis.setPixmap(pixmap_syn)
        self.synopsis.mousePressEvent = self.getPos
        self.total_length = 880 # synopsis from 0 to 880

        #self.frames = []
        #for num in range(299, 300):
        #    fileName = "image-"+str(num).zfill(4)+".rgb"
        #    #print(fileName)
        #    video = readrgb.readrgbtoQImage(self.folderName+fileName)
        #    #pixmap_vdo = QPixmap.fromImage(video)
        #    self.frames.append( QPixmap.fromImage(video) )

        self.sound = QVideoWidget()
        self.sound.setGeometry(QtCore.QRect(859, 10, 111, 21))
        self.sound.setObjectName("sound")

        self.soundPlayer = QMediaPlayer(None, QMediaPlayer.LowLatency)
        #self.soundPlayer.setVideoOutput(videoWidget)
        #self.soundPlayer.stateChanged.connect(self.mediaStateChanged)
        #self.soundPlayer.positionChanged.connect(self.positionChanged)
        #self.soundPlayer.durationChanged.connect(self.durationChanged)
        #self.soundPlayer.error.connect(self.handleError)

        #fileName = "video_1.avi"
        #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
        self.soundPlayer.setAudioRole(2)
        self.soundPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("video_1.wav")))

        self.v_thread = Img_Thread(self.updateframe)

        
       
    def play(self):
        print("play")
        self.paused = 0
        if self.soundPlayer.state() != QMediaPlayer.PlayingState:
            self.soundPlayer.play()
        self.image_thread()


    def updateframe(self):
        print(self.current_frame)
        fileName = "image-"+str(self.current_frame).zfill(4)+".rgb"
        video = readrgb.readrgbtoQImage(self.folderName+fileName)
        pixmap_vdo = QPixmap.fromImage(video)
        self.video.setPixmap(pixmap_vdo)
        #self.video.repaint()
        self.current_frame += 1
        

    def image_thread(self):
        
        self.v_thread.n = self.end_frame - self.current_frame
        self.v_thread.kill = 0
        self.v_thread.start()


    def pause(self):
        print("pause")
        if self.soundPlayer.state() == QMediaPlayer.PlayingState:
            self.soundPlayer.pause()
        self.v_thread.kill = 1
        

    def stop(self):
        print("stop")
        if self.soundPlayer.state() != QMediaPlayer.StoppedState:
            self.soundPlayer.stop()
        self.v_thread.kill = 1
        self.current_frame = self.end_frame


    def getPos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print(str(x)+"  "+str(y))
        #print(x)
        self.start_frame = 1
        self.start_time = 1
        self.end_frame = 1000
        self.current_frame = self.start_frame
        #video = QtGui.QMovie("test.gif")
        #self.video.setMovie(video)
        #video.start()
        self.soundPlayer.setPosition(1)
        self.soundPlayer.play()
        self.play()
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


