import numpy as np
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt6.QtGui import QPixmap, QPainter, QPen, QImage, QColor, QVector2D
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QRectF, QLineF, QLine
import sys, math, socket, zss_debug_pb2, MATRIX
from UDP import ADDRESS, PORT
from color import COLOR

debugPointSize = 3
carDiameter = 180
carFaceWidth = 120


class UDPReceiveBlue(QThread):
    receive_debug_signal = pyqtSignal(np.ndarray)
    debug_msgs = zss_debug_pb2.Debug_Msgs()
    def __init__(self):
        super().__init__()
        self._receive_flag = True
        self.sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)
        self.sock.bind((ADDRESS.LOCAL_HOST, PORT.BLUE_DEBUG))
    def run(self):
        while True:
            proto_data, addr = self.sock.recvfrom(65535)
            self.debug_msgs.ParseFromString(proto_data)
            self.receive_debug_signal.emit(np.array(1))


    def stop(self):
        self._run_flag = False
        self.wait()

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
        self.label_board = QLabel(self)
        self.label_board.setGeometry(0, 0, 1500, 1500)
        self.image_label.setPixmap(QPixmap.fromImage(QImage('images/Sat Nov 25 17:43:20 2023.png').scaled(self.disply_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)))
        self.label_debug_msg = QLabel(self)
        self.label_debug_msg.setGeometry(0, 0, 1500, 1500)

        self.pos1 = [0, 0]
        self.pos2 = [0, 0]

        self.thread = UDPReceiveBlue()
        self.thread.receive_debug_signal.connect(self.update_debug_msgs)
        self.thread.start()

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
        pixmap = QPixmap(self.label_board.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        qp = QPainter(pixmap)
        qp.setTransform(MATRIX.BOARD_TRANSFORM)
        pen = QPen(COLOR.DEBUG[1], 5)           # red
        qp.setPen(pen)
        qp.drawLine(self.pos1[0], self.pos1[1], self.pos2[0], self.pos2[1])
        qp.end()
        self.label_board.setPixmap(pixmap)

    # @pyqtSlot(np.ndarray)
    def update_debug_msgs(self):
        pixmap = QPixmap(self.label_debug_msg.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        qp = QPainter(pixmap)
        qp.setTransform(MATRIX.DEBUG_TRANSFORM)
        i = 0
        chordAngel = math.degrees(math.acos(1.0 * carFaceWidth / carDiameter))
        while i < len(self.thread.debug_msgs.msgs):
            msg = self.thread.debug_msgs.msgs[i]
            if msg.color == zss_debug_pb2.Debug_Msg.Color.USE_RGB:
                value = msg.RGB_value
                rgb = [0, 0, 0]
                for j in range (0, 3):
                    rgb[2 - j] = value % 1000
                    value = (value - rgb[2 - j]) / 1000
                    if rgb[2 - j] > 255 or rgb[2 - j] < 0:      # error value
                        rgb = [0, 0, 0]
                        break
                qp.setPen(QPen(QColor(rgb[0], rgb[1], rgb[2]), 10))
            else:
                qp.setPen(QPen(COLOR.DEBUG[msg.color], 10))
            if msg.type == zss_debug_pb2.Debug_Msg.Debug_Type.ROBOT:
                qp.drawChord(QRectF((msg.robot.pos.x - 1.2 * carDiameter / 2.0),
                    (msg.robot.pos.y) + 1.2 * carDiameter / 2.0,(1.2 * carDiameter),
                    -(1.2 * carDiameter)),90.0 - chordAngel - msg.robot.dir,180.0 + 2 * chordAngel);
            elif msg.type == zss_debug_pb2.Debug_Msg.Debug_Type.LINE:
                qp.drawLine(msg.line.start.x, msg.line.start.y, msg.line.end.x, msg.line.end.y)
            elif msg.type == zss_debug_pb2.Debug_Msg.Debug_Type.ARC:
                x1 = msg.arc.rect.point1.x
                x2 = msg.arc.rect.point2.x
                y1 = msg.arc.rect.point1.y
                y2 = msg.arc.rect.point2.y
                minx = min(x1, x2)
                miny = min(y1, y2)
                maxx = max(x1, x2)
                maxy = max(y1, y2)
                qp.drawArc(QRectF(float(minx), (float(miny)), ((maxx - minx)), ((maxy - miny))), msg.arc.start * 16,
                           msg.arc.span * 16)
            elif msg.type == zss_debug_pb2.Debug_Msg.Debug_Type.POINTS:
                lines = QVector2D(QLine)
                for j in range(0, len(msg.points())):
                    lines.push_back(QLine((msg.points().point(i).x() + debugPointSize),
                                          (msg.points().point(i).y() + debugPointSize),
                                          (msg.points().point(i).x() - debugPointSize),
                    (msg.points().point(i).y() - debugPointSize)))
                    lines.push_back(QLine((msg.points().point(i).x() - debugPointSize),
                    (msg.points().point(i).y() + debugPointSize),(msg.points().point(i).x() + debugPointSize),
                    (msg.points().point(i).y() - debugPointSize)))
                qp.drawLines(lines);
            elif msg.type == zss_debug_pb2.Debug_Msg.Debug_Type.LINES:
                lines = QVector2D(QLine)
                step = 1 if msg.lines().type() == zss_debug_pb2.Debug_Msg.Debug_Lines.LINE else 2
                for j in range (1, len(msg.lines(), step)):
                    lines.append(QLineF((msg.lines().vertex(j - 1).x()),msg.lines().vertex(j - 1).y(),
                    msg.lines().vertex(j).x(),msg.lines().vertex(j).y()))
                qp.drawLine(lines)
            i += 1

        qp.end()
        self.label_debug_msg.setPixmap(pixmap)


    # def __paint_line__(self, qp, debug_msgs):
    #     pen = debug_msgs.color()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())