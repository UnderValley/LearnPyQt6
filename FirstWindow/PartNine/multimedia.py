from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt6.QtGui import QPixmap
import sys
import cv2
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    webcamindex = 0

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.webcamindex)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)

        # self.btn_start = QPushButton("Start")
        # self.btn_close = QPushButton("Close")

        self.combobox = QComboBox()
        self.webcam_detect()
        # self.combobox.currentTextChanged.connect(self.select_webcam)
        # self.combobox.addItem("1")

        hbox.addWidget(self.combobox)
        # hbox.addWidget(self.btn_start)
        # hbox.addWidget(self.btn_close)
        # self.btn_start.clicked.connect(self.link_start)
        # self.btn_close.clicked.connect(self.link_close)

        self.setLayout(hbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()



    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def webcam_detect(self):
        i = 0
        capdetect = cv2.VideoCapture(i)
        while capdetect.isOpened() :
            i += 1
            capdetect.release()
            capdetect = cv2.VideoCapture(i)
        capdetect.release()
        for a in range(0, i):
            self.combobox.addItem(str(a))

    # def select_webcam(self):
        # self.thread.quit()
        # self.thread = VideoThread()
        # self.thread.webcamindex = int(self.combobox.currentText())
        # self.textLabel.setText(self.combobox.currentText())

    # def link_start(self):
    #
    #     self.thread.start()
    #
    # def link_close(self):
    #     self.thread.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec())