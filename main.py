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
            #print("i"+str(i))
            if self.kill == 1:
                break
            try:
                self.fn()
            except Exception as e:
                break
            if i == self.n-1:
                self.signal.emit(0)
            self.msleep(33)
        

class MyQtApp(multimediaUI.Ui_MainWindow, QtWidgets.QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Multimedia Project")
        #self.import_PB.clicked.connect(self.openFile)
        #self.toolButton.clicked.connect(self.openFile)

        #self.folderName = "../../576RGBVideo1/"
        # self.folderName = "/Users/luckyjustin/Documents/JustinProject/576Project/CSCI576ProjectMedia/576RGBVideo1/"
        self.play_btn.clicked.connect(self.play)
        self.pause_btn.clicked.connect(self.pause)
        self.stop_btn.clicked.connect(self.stop)
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        
        synopsis = readrgb.readrgbtoQImage("test.rgb", 352*25, 288)
        #print(self.synopsis.size())
        pixmap_syn = QPixmap.fromImage(synopsis).scaled(3000, 1440, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #pixmap_syn.scaledToHeight(100)
        self.synopsis.setPixmap(pixmap_syn)
        self.synopsis.mousePressEvent = self.getPos
        #self.total_length = 880 # synopsis from 0 to 880

        self.sound = QVideoWidget()
        self.sound.setGeometry(QtCore.QRect(859, 10, 111, 21))
        self.sound.setObjectName("sound")

        self.soundPlayer = QMediaPlayer(None, QMediaPlayer.LowLatency)
        self.soundPlayer.setAudioRole(2)
        #self.soundPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("video_1.wav")))
        # self.soundPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("/Users/luckyjustin/Documents/JustinProject/576Project/CSCI576ProjectMedia/video_1.wav")))
        self.v_thread = Img_Thread(self.updateframe)
        self.v_thread.signal.connect(self.stop)

        
       
    def play(self):
        #print("play")
        if self.soundPlayer.state() != QMediaPlayer.PlayingState:
            self.soundPlayer.play()
        self.image_thread()
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)


    def updateframe(self):
        #print(self.current_frame)
        fileName = "image-"+str(self.current_frame).zfill(4)+".rgb"
        video = readrgb.readrgbtoQImage(self.folderName+fileName)
        pixmap_vdo = QPixmap.fromImage(video)
        self.video.setPixmap(pixmap_vdo)
        #self.video.repaint()
        self.current_frame += 1
        
    def image_thread(self):
        self.v_thread.n = self.end_frame - self.current_frame +1
        self.v_thread.kill = 0
        self.v_thread.start()

    def pause(self):
        #print("pause")
        if self.soundPlayer.state() == QMediaPlayer.PlayingState:
            self.soundPlayer.pause()
        self.v_thread.kill = 1
        self.play_btn.setEnabled(True)
        
    def stop(self):
        #print("stop")
        if self.soundPlayer.state() != QMediaPlayer.StoppedState:
            self.soundPlayer.stop()
        self.v_thread.kill = 1
        self.current_frame = self.end_frame
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)

    def show_img(self):
        if self.soundPlayer.state() != QMediaPlayer.StoppedState:
            self.stop()
        video = readrgb.readrgbtoQImage(self.fileName)
        pixmap_vdo = QPixmap.fromImage(video)
        self.video.setPixmap(pixmap_vdo)


    def play_video(self):
        self.current_frame = self.start_frame
        self.soundPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))
        self.soundPlayer.setPosition(1)
        self.play()

    def getfiles(self, idx):
        # for video
        self.folderName = "../../576RGBVideo1/"
        self.start_frame = 1
        self.end_frame = 1000
        self.start_time = 1
        self.audio_file = "video_1.wav"
        # for image
        self.fileName = "image-0003.rgb"
        return idx < 1000 # tp = 1: video ; tp = 0: image

    def getPos(self, event):
        x = event.pos().x()
        print(x)
        tp = self.getfiles(x//1)
        if self.soundPlayer.state() == QMediaPlayer.PlayingState:
            self.v_thread.kill = 1
            #self.stop()
            time.sleep(0.03) # for racing
        if tp:
            self.play_video()
        else:
            self.show_img()
        
        
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


