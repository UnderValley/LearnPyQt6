from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle("Python GUI Development")

        self.create_widget()

    def create_widget(self):
        hbox = QHBoxLayout()
        btn = QPushButton("Change Text")
        btn.clicked.connect(self.clicked_btn)
        self.label = QLabel("Default Text")
        hbox.addWidget(btn)
        hbox.addWidget(self.label)
        self.setLayout(hbox)

    def clicked_btn(self):
        self.label.setText("Another Text")
        self.label.setFont(QFont(QFont("Times", 15, QFont.Weight.ExtraBold)))
        self.label.setStyleSheet('color:red')


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())