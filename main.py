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
import json
import os

class Img_Thread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, fn):
        QThread.__init__(self)
        self.fn = fn
        self.n = 0
        self.kill = 0

    def run(self):
        for i in range(self.n):
            #print("i= "+str(i))
            if self.kill == 1:
                break
            try:
                self.fn()
            except Exception as e:
                print(e)
                continue
            if i == self.n-1:
                self.signal.emit(0)
            #self.msleep(32)

class MyQtApp(multimediaUI.Ui_MainWindow, QtWidgets.QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Multimedia Project")

        self.play_btn.clicked.connect(self.play)
        self.pause_btn.clicked.connect(self.pause)
        self.stop_btn.clicked.connect(self.stop)
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        
        #read metadata
        file_meta = open('final.json',"r")
        self.metadata = json.load(file_meta)
        self.num_img = len(self.metadata)
        file_meta.close()
        print(self.num_img)

        # synopsis = readrgb.readrgbtoQImage("version2_synopsis.rgb", 352*self.num_img, 288)
        synopsis = readrgb.readrgbtoQImage("final.rgb", 352*self.num_img, 288)
        #print(self.synopsis.size())
        self.total_length = 120*self.num_img # synopsis from 0 to total length
        pixmap_syn = QPixmap.fromImage(synopsis).scaled(120*self.num_img, 1440, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.synopsis.setPixmap(pixmap_syn)
        self.synopsis.mousePressEvent = self.getPos
        
        self.sound = QVideoWidget()
        self.sound.setGeometry(QtCore.QRect(859, 10, 111, 21))
        self.sound.setObjectName("sound")

        self.soundPlayer = QMediaPlayer(None, QMediaPlayer.LowLatency)
        self.soundPlayer.setAudioRole(2)

        self.v_thread = Img_Thread(self.updateframe)
        self.v_thread.signal.connect(self.stop)
        self.v_thread.n = 0
        self.v_thread.start()

        self.sound_delay = 0
        
       
    def play(self):
        #print("play")
        #if self.soundPlayer.state() != QMediaPlayer.PlayingState:
        #print(self.soundPlayer.position()/1000)
        #time.sleep(0.05)
        #print(self.v_thread.isFinished())
        self.thistimestart_frame = self.current_frame -1
        self.soundPlayer.play()
        #time.sleep(self.sound_delay) # wait for the sound track to play
        while self.soundPlayer.position() <= 1:
            pass
        self.tic = time.perf_counter()
        self.image_thread()
        #self.soundPlayer.play()
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)

    def updateframe(self):
        #print(self.current_frame)
        fileName = "image-"+str(self.current_frame).zfill(4)+".rgb"
        video = readrgb.readrgbtoQImage(self.folderName+fileName)
        pixmap_vdo = QPixmap.fromImage(video)

        # sync to sound position
        delay = self.current_frame/30 - self.soundPlayer.position()/1000
        if delay > 0:
            #print("wait", delay)
            time.sleep(delay)
        elif delay < - 0.03:
            print("late", delay)
        

        '''
        # absolute time
        ontime = (self.current_frame - self.thistimestart_frame )/30
        delay = time.perf_counter() - self.tic
        if delay < ontime:
            #if (ontime-delay) > 0.033:
            #    print("long wait", ontime-delay)
            time.sleep(ontime - delay)
        elif delay-ontime > 0.5:
            print("too late", delay-ontime)
        '''
            
        
        self.video.setPixmap(pixmap_vdo)
        #print(self.current_frame)
        self.current_frame += 1
        
    def image_thread(self):
        self.v_thread.n = self.end_frame - self.current_frame +1
        self.v_thread.kill = 0
        self.v_thread.start()

    def pause(self):
        #print("pause")

        #if self.soundPlayer.state() == QMediaPlayer.PlayingState:
        self.soundPlayer.pause()
        self.v_thread.kill = 1
        
        time.sleep(0.04)
        #print(self.v_thread.isFinished())
        print(self.current_frame)
        self.current_frame = self.soundPlayer.position()*30//1000+1
        print(self.current_frame)

        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        
    def stop(self):
        #print("stop")
        if self.soundPlayer.state() != QMediaPlayer.StoppedState:
            self.soundPlayer.pause()
            #print(self.soundPlayer.position()/1000)
            #print(self.soundPlayer.position()/1000 - self.end_frame/30)
        self.v_thread.kill = 1
        self.current_frame = self.start_frame
        self.soundPlayer.setPosition(self.start_time)
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)

    def show_img(self):
        if self.soundPlayer.state() != QMediaPlayer.StoppedState:
            self.stop()
            self.play_btn.setEnabled(False)
        video = readrgb.readrgbtoQImage("."+self.fileName)
        pixmap_vdo = QPixmap.fromImage(video)

        self.video.setPixmap(pixmap_vdo)
        self.Displaying.setText("Displaying Image: " + self.fileName)

    def play_video(self):
        self.current_frame = self.start_frame
        self.soundPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath(self.audio_file)))) # mac
        # self.soundPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))
        self.soundPlayer.setPosition(self.start_time)
        fileName = "image-"+str(self.start_frame).zfill(4)+".rgb"
        video = readrgb.readrgbtoQImage(self.folderName+fileName)
        pixmap_vdo = QPixmap.fromImage(video)
        self.current_frame += 1
        self.video.setPixmap(pixmap_vdo)
        self.Displaying.setText("Displaying Video: " + self.folderName)
        self.play()

    def getfiles(self, idx):
        #print(idx)
        if idx >= self.num_img:
            idx = self.num_img-1
        tp = self.metadata[idx]["tp"] # tp = 1: video ; tp = 0: image
        if tp == 1:
            # for video
            self.folderName = "."+self.metadata[idx]["folder"] #"../../576RGBVideo1/"
            # self.folderName = "/Users/luckyjustin/Documents/JustinProject/576Project/CSCI576ProjectMedia/576RGBVideo1/"
            self.start_frame = self.metadata[idx]["start"] #1
            self.end_frame = self.metadata[idx]["end"] #1000
            self.start_time = (self.start_frame-1)*1000/30
            self.audio_file = "."+self.metadata[idx]["audio"] #"video_1.wav"
            #self.audio_file = "/Users/luckyjustin/Documents/JustinProject/576Project/CSCI576ProjectMedia/video_1.wav"
            #print(self.folderName)
            #print(self.audio_file)
            #print("start frame = " + str(self.start_frame/30))
            #print("end frame = " + str(self.end_frame/30))

        else:
            # for image
            self.fileName = self.metadata[idx]["path"] #"image-0003.rgb"
        return tp # tp = 1: video ; tp = 0: image

    def getPos(self, event):
        x = event.pos().x()
        #print(x)
        tp = self.getfiles(x//120) # x//(width of an image = 120)
        if self.soundPlayer.state() == QMediaPlayer.PlayingState:
            self.v_thread.kill = 1
            time.sleep(0.04) # for racing
        if tp:
            self.play_video()
        else:
            self.show_img()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    qt_app = MyQtApp()
    qt_app.show()
    sys.exit(app.exec_())

