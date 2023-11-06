from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt6.QtGui import QPixmap
import sys
import cv2
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import time


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    webcam_index = 204     #change the index to select webcam
    shoot_flag = 0
    pic_filename = "images/" + str(time.asctime( time.localtime(time.time()) )) + ".png"
    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.webcam_index)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while self._run_flag:
            ret, cv_img = cap.read()
            if self.shoot_flag == 1:
                cv2.imwrite(self.pic_filename, cv_img)
                self.shoot_flag = 0
                self.pic_filename = "images/" + str(time.asctime(time.localtime(time.time()))) + ".png"
            # cv_img = cv2.resize(cv_img, (4000, 3000))
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
        self.disply_width = 640 * 2
        self.display_height = 480 * 2
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
        self.btnshot = QPushButton("Shoot")
        # self.webcam_detect()
        # self.combobox.currentTextChanged.connect(self.select_webcam)
        # self.combobox.addItem("1")

        hbox.addWidget(self.combobox)
        hbox.addWidget(self.btnshot)
        # hbox.addWidget(self.btn_start)
        # hbox.addWidget(self.btn_close)
        # self.btn_start.clicked.connect(self.link_start)
        # self.btn_close.clicked.connect(self.link_close)

        self.btnshot.clicked.connect(self.cam_shoot)
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

    # @pyqtSlot(np.ndarray)
    def cam_shoot(self):
         self.thread.shoot_flag = 1


    # def webcam_detect(self):

    # def select_webcam(self):

    # def link_start(self):



if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec())