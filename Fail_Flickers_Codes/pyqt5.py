from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QMovie, QFont
from PyQt5 import QtTest
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import sys
import os

class Ui_MainWindow(object):

    centralwidget = None
    labelGif1 = None
    labelGif2 = None
    labelGif3 = None
    labelGif4 = None
    w = 1250
    h = 700
    labelText = None
    texts = ["Primer rectangulo", "Segundo rectangulo", "Tercer rectangulo", "Cuarto rectangulo"]

    def runPrueba(self, MainWindow):
        #self.setupEnv(MainWindow)
        """ self.showTest(self.texts[0])
        
        QtTest.QTest.qWait(3000)

        self.removeText() """
        
        #self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.showVideo(MainWindow)
        """ movie1 = self.showGif(self.labelGif1, 25,25,'video_10hz.mp4')
        movie2 = self.showGif(self.labelGif2, 2550,25,'10hz_flick.gif')
        movie3 = self.showGif(self.labelGif3,25, 1400,'12hz_flick.gif')
        movie4 = self.showGif(self.labelGif4,2550,1400,'15hz_flick.gif')
        self.startMovie(movie1)
        self.startMovie(movie2)
        self.startMovie(movie3)
        self.startMovie(movie4) """
        #MainWindow.setCentralWidget(self.centralwidget)
        
    def setupEnv(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
    
    def showTest(self, text):
        self.labelText = QtWidgets.QLabel(text=text,parent=self.centralwidget)
        self.labelText.setFont(QFont('Arial', 45))
        self.labelText.move(1350,950)
    
    def removeText(self):
        self.labelText.setParent(None)

    def showVideo(self,MainWindow):
        video_widget = QVideoWidget()
        MainWindow.setCentralWidget(video_widget)
        self.player = QMediaPlayer(MainWindow, QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(video_widget)
        path = os.path.join(os.path.dirname(__file__), "video_10hz.mp4")
        self.player.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(path)))
        self.player.play()

    def showGif(self, label, cordX, cordY, gifName):
        label = QtWidgets.QLabel(self.centralwidget)
        label.setGeometry(QtCore.QRect(cordX, cordY, self.w, self.h))
        self.movie = QMovie(gifName)
        label.setMovie(self.movie)
        return self.movie
    
    def startMovie(self, movie):
        movie.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.showFullScreen()
    window.setCursor(QtCore.Qt.CursorShape.BlankCursor)
    ui = Ui_MainWindow()
    ui.runPrueba(window)
    window.show()
    sys.exit(app.exec_())