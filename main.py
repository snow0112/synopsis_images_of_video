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
       
    def play(self):
        print("play")
        self.paused = 0
        if self.soundPlayer.state() != QMediaPlayer.PlayingState:
            self.soundPlayer.play()

        while 1: # self.soundPlayer.state() == QMediaPlayer.PlayingState:
            fileName = "image-"+str(self.current_frame).zfill(4)+".rgb"
            #print(fileName)
            video = readrgb.readrgbtoQImage(self.folderName+fileName)
            pixmap_vdo = QPixmap.fromImage(video)
            self.video.setPixmap(pixmap_vdo)
            self.video.repaint()
            break
            if self.current_frame == self.end_frame:
                self.soundPlayer.stop()
                break
            self.current_frame += 1
            time.sleep(0.03333)


    def pause(self):
        print("pause")
        if self.soundPlayer.state() == QMediaPlayer.PlayingState:
            self.soundPlayer.pause()
        
        #for frame in self.frames:
        #    self.video.setPixmap(frame)
        #    self.video.repaint()
        #    time.sleep(0.03333)  

    def stop(self):
        print("stop")
        if self.soundPlayer.state() != QMediaPlayer.StoppedState:
            self.soundPlayer.stop()
        self.current_frame = self.end_frame
        #video = QImage(352, 288, QImage.Format_RGB32)
        #pixmap_vdo = QPixmap.fromImage(video)
        #self.video.setPixmap(pixmap_vdo)
        #self.video.repaint()

    def getPos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print(str(x)+"  "+str(y))
        #print(x)
        self.start_frame = 1
        self.start_time = 1
        self.end_frame = 100
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


