from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt6.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt6.QtCore import Qt
import sys



class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640 * 2
        self.display_height = 480 * 2
        self.setGeometry(200, 200, 640 * 2, 480 * 2)
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(11, 285, self.disply_width, self.display_height)
        self.setMouseTracking(True)

        self.label1 = QLabel("Press", self)
        self.label2 = QLabel("Release", self)
        self.label1.setGeometry(1240, 370, 100, 100)
        self.label2.setGeometry(1240, 1140, 100, 100)
        self.label_top = QLabel(self)
        self.label_top.setGeometry(self.image_label.pos().x(),self.image_label.pos().y() ,self.image_label.size().width(),self.image_label.size().height())
        self.image_label.setPixmap(QPixmap.fromImage(QImage('images/Sat Nov 25 17:43:20 2023.png').scaled(self.disply_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)))

        self.pos1 = [0, 0]
        self.pos2 = [0, 0]

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawRect(1400, 200, 900, 1200)
        # painter.setPen(QPen(Qt.GlobalColor.black, 5, Qt.PenStyle.SolidLine))
        painter.drawLine(self.pos1[0], self.pos1[1], self.pos2[0], self.pos2[1])
        painter.end()
        self.set_Label()

    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.pos1[0], self.pos1[1] = self.cursor().pos().x() - self.x(), self.cursor().pos().y() - self.y() - 38
            self.pos2[0], self.pos2[1] = self.cursor().pos().x() - self.x(), self.cursor().pos().y() - self.y() - 38
            self.label1.setText("{0}, {1}".format(self.pos1[0], self.pos1[1]))
            self.update()


    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.pos2[0], self.pos2[1] = self.cursor().pos().x() - self.x(), self.cursor().pos().y() - self.y() - 38
            self.label2.setText("{0}, {1}".format(self.pos2[0], self.pos2[1]))
            self.update()

    def set_Label(self):
        pixmap = QPixmap(self.label_top.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        qp = QPainter(pixmap)
        pen = QPen(Qt.GlobalColor.red, 3)
        qp.setPen(pen)
        qp.drawLine(self.pos1[0]-1000, self.pos1[1], self.pos2[0]-1000, self.pos2[1])
        qp.end()
        self.label_top.setPixmap(pixmap)

    # def mouseReleaseEvent(self, event):
        # self.pos2[0], self.pos2[1] = self.cursor().pos().x() - self.x(), self.cursor().pos().y() - self.y() - 38
        # self.label2.setText("{0}, {1}".format(self.pos2[0], self.pos2[1]))
        # self.update()

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())