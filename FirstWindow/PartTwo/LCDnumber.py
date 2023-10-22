from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMenu, QLCDNumber, QVBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize, QTime, QTimer
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle("PyQt6 QPushButton")

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.show_LCD)
        # self.timer.start(1000)

        # self.show_LCD()


    def show_LCD(self):

        lcd = QLCDNumber()
        vbox = QVBoxLayout()
        vbox.addWidget(lcd)

        lcd.setStyleSheet('background:red')

        time = QTime.currentTime()
        lcd.display(time.toString('hh:mm:ss'))

        self.setLayout(vbox)



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())