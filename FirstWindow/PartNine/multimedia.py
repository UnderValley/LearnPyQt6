from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt6.QtGui import QPixmap, QPainter, QPen, QImage
import sys
import cv2
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import time

mtx = np.array([[329.27575738, 0, 347.99824656], [0, 328.85582461, 219.0933177 ], [0, 0, 1]])
dist = np.array([-3.39635228e-01, 1.58532494e-01, 7.93601798e-04, 1.17840905e-04, -4.30169501e-02])
tr_matrix = np.array([[ 3.16260888e-02, -3.30701236e-01,  4.19977106e+02],
 [-1.09647099e-01, -1.31679696e-01,  4.87941764e+02],
 [-2.41137870e-04, -2.91447781e-04,  1.00000000e+00]])  # perspective transformation matrix

def undist(img):
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    # dst = cv2.resize(dst, (20 * w, 20 * h), interpolation=cv2.INTER_CUBIC)
    return dst
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
            cv_img = undist(cv_img)
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
        self.image_label.setGeometry(11, 285, self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')
        self.setMouseTracking(True)

        self.label1 = QLabel("Press", self)
        self.label2 = QLabel("Release", self)
        self.label1.setGeometry(1240, 370, 100, 100)
        self.label2.setGeometry(1240, 1140, 100, 100)
        self.label_top = QLabel(self)
        self.label_top.setGeometry(0, 0, 1500, 1500)

        # self.combobox = QComboBox(self)
        self.btnshot = QPushButton("Shoot", self)
        self.btnshot.setGeometry(1240, 700, 50, 20)
        self.btnshot.clicked.connect(self.cam_shoot)

        self.pos1 = [0, 0]
        self.pos2 = [0, 0]

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
        # qp.drawLine(self.pos1[0], self.pos1[1], self.pos2[0], self.pos2[1])
        output_point1 = self.perTransform(self.pos1)
        output_point2 = self.perTransform(self.pos2)
        qp.drawLine(output_point1[0], output_point1[1], output_point2[0], output_point2[1])
        self.label1.setText("{0}, {1}\n{2}, {3}".format(self.pos1[0], self.pos1[1], int(output_point1[0]), int(output_point1[1])))
        qp.end()
        '''
        transfer = QTransform(3.16260888e-02, -3.30701236e-01,  4.19977106e+02,-1.09647099e-01, -1.31679696e-01,  4.87941764e+02, -2.41137870e-04, -2.91447781e-04,  1.00000000e+00)
        # transfer = transfer.setMatrix(3.16260888e-02, -3.30701236e-01,  4.19977106e+02,-1.09647099e-01, -1.31679696e-01,  4.87941764e+02, -2.41137870e-04, -2.91447781e-04,  1.00000000e+00)
        pixmap = pixmap.transformed(transfer)
        '''
        self.label_top.setPixmap(pixmap)

    def perTransform(self, p):
        result = np.matmul(tr_matrix, np.array([p[0], p[1], 1]))
        result = result / result[2]
        return [result[0], result[1]]

    # def webcam_detect(self):

    # def select_webcam(self):

    # def link_start(self):



if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec())