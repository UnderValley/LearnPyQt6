from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle("Python GUI Development")
        '''
        # 简单文字label显示
        label = QLabel("Python Gui development", self)
        label.setText("New Text is Here")
        label.move(100, 100)
        label.setFont(QFont("Sanserif", 15))
        label.setStyleSheet('color:red')
        '''
        '''
        # 图片显示
        label = QLabel(self)
        pixmap = QPixmap('Image/Chihaya Anon.png')
        label.setPixmap(pixmap)
        '''
        '''
        # 播放gif或movie
        label = QLabel(self)
        movie = QMovie('')
        movie.setSpeed(500)
        label.setMovie(movie)
        movie.start()
        '''

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())