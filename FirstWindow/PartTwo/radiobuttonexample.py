from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QRadioButton, QLabel, QVBoxLayout
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie
from PyQt6.QtCore import QSize
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle("PyQt6 QHBoxLayout")

        self.create_radio()

    def create_radio(self):
        self.hbox = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        self.rad1 = QRadioButton("Chihaya Anon")
        self.rad1.setIcon(QIcon("Image/Chihaya Anon.png"))
        self.rad1.setIconSize(QSize(40,40))
        # rad1.setFont()
        # rad1.setChecked(True)
        self.rad1.toggled.connect(self.radio_selected)

        self.rad2 = QRadioButton("Takamatsu Tomori")
        self.rad2.setIcon(QIcon("Image/Takamatsu Tomori.png"))
        self.rad2.setIconSize(QSize(40, 40))
        # rad1.setFont()
        # rad2.setChecked(False)
        self.rad2.toggled.connect(self.radio_selected)

        self.rad3 = QRadioButton("Chihaya Anon")
        self.rad3.setIcon(QIcon("Image/Chihaya Anon.png"))
        self.rad3.setIconSize(QSize(40, 40))
        # rad1.setFont()
        # rad1.setChecked(True)
        self.rad3.toggled.connect(self.radio_selected)

        self.rad4 = QRadioButton("Takamatsu Tomori")
        self.rad4.setIcon(QIcon("Image/Takamatsu Tomori.png"))
        self.rad4.setIconSize(QSize(40, 40))
        # rad1.setFont()
        # rad2.setChecked(False)
        self.rad4.toggled.connect(self.radio_selected)

        self.label = QLabel("Character")
        self.label.setFont(QFont("Times", 15))

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox2)

        self.hbox.addWidget(self.rad1)
        self.hbox.addWidget(self.rad2)

        self.hbox2.addWidget(self.rad3)
        self.hbox2.addWidget(self.rad4)

        self.setLayout(self.vbox)

    def radio_selected(self):
        selected1 = ""
        selected2 = ""

        if self.rad1.isChecked():
            selected1 = self.rad1.text()
        if self.rad2.isChecked():
            selected1 = self.rad2.text()
        if self.rad3.isChecked():
            selected2 = self.rad3.text()
        if self.rad4.isChecked():
            selected2 = self.rad4.text()

        self.label.setText("You've choosed " + selected1 + "&" + selected2)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())