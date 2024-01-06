import numpy as np
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QCheckBox, QComboBox, QPushButton
from PyQt6.QtGui import QPixmap, QPainter, QPen, QImage, QColor, QVector2D, QIcon, QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QRectF, QLineF, QLine, QMutex, QPoint
import sys, math, socket, zss_debug_pb2, MATRIX
from UDP import ADDRESS, PORT
from color import COLOR

debugPointSize = 3
carDiameter = 180
carFaceWidth = 120
penSize = 30

mutex_blue = QMutex()
mutex_yellow = QMutex()

def update_one_frame(thread, isBlue):
    if isBlue == 1:
        mutex_blue.lock()
        thread.debug_msgs.ParseFromString(thread.win.blue_debug_thread.prodata)
        mutex_blue.unlock()
        pixmap = QPixmap(thread.win.label_blue_debug_msg.size())
    else:
        mutex_yellow.lock()
        thread.debug_msgs.ParseFromString(thread.win.yellow_debug_thread.prodata)
        mutex_yellow.unlock()
        pixmap = QPixmap(thread.win.label_yellow_debug_msg.size())
    pixmap.fill(Qt.GlobalColor.transparent)
    qp = QPainter(pixmap)
    qp.setTransform(MATRIX.DEBUG_TRANSFORM)
    i = 0
    chordAngel = math.degrees(math.acos(1.0 * carFaceWidth / carDiameter))
    while i < len(thread.debug_msgs.msgs):
        # print(i, len(thread.blue_debug_thread.debug_msgs.msgs))
        msg = thread.debug_msgs.msgs[i]
        if msg.color == zss_debug_pb2.Debug_Msg.Color.USE_RGB:
            value = msg.RGB_value
            rgb = [0, 0, 0]
            for j in range(0, 3):
                rgb[2 - j] = value % 1000
                value = (value - rgb[2 - j]) / 1000
                if rgb[2 - j] > 255 or rgb[2 - j] < 0:  # error value
                    rgb = [0, 0, 0]
                    break
            qp.setPen(QPen(QColor(rgb[0], rgb[1], rgb[2]), penSize))
        else:
            qp.setPen(QPen(COLOR.DEBUG[msg.color], penSize))
        if msg.type == zss_debug_pb2.Debug_Msg.Debug_Type.ROBOT:
            qp.drawChord(QRectF((msg.robot.pos.x - 1.2 * carDiameter / 2.0),
                                (msg.robot.pos.y) + 1.2 * carDiameter / 2.0, (1.2 * carDiameter),
                                -(1.2 * carDiameter)), 90.0 - chordAngel - msg.robot.dir,
                         180.0 + 2 * chordAngel)
        elif (msg.type == zss_debug_pb2.Debug_Msg.Debug_Type.LINE and not math.isnan(msg.line.start.x)
              and not math.isnan(msg.line.start.y) and not math.isnan(msg.line.end.x) and not math.isnan(msg.line.start.y)):
            p1 = QPoint(int(msg.line.start.x), int(msg.line.start.y))
            p2 = QPoint(int(msg.line.end.x), int(msg.line.end.y))
            qp.drawLine(p1, p2)
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
                lines.push_back(QLine((msg.points().point(j).x() + debugPointSize),
                                      (msg.points().point(j).y() + debugPointSize),
                                      (msg.points().point(j).x() - debugPointSize),
                                      (msg.points().point(j).y() - debugPointSize)))
                lines.push_back(QLine((msg.points().point(j).x() - debugPointSize),
                                      (msg.points().point(j).y() + debugPointSize),
                                      (msg.points().point(j).x() + debugPointSize),
                                      (msg.points().point(j).y() - debugPointSize)))
            qp.drawLines(lines)
        elif msg.type == zss_debug_pb2.Debug_Msg.Debug_Type.LINES:
            lines = QVector2D(QLine)
            step = 1 if msg.lines().type() == zss_debug_pb2.Debug_Msg.Debug_Lines.LINE else 2
            for j in range(1, len(msg.lines()), step):
                lines.append(QLineF((msg.lines().vertex(j - 1).x()), msg.lines().vertex(j - 1).y(),
                                    msg.lines().vertex(j).x(), msg.lines().vertex(j).y()))
            qp.drawLine(lines)
        i = i + 1

    qp.end()
    if isBlue == 1:
        thread.win.label_blue_debug_msg.setPixmap(pixmap)
    else:
        thread.win.label_yellow_debug_msg.setPixmap(pixmap)

class UDPReceiveBlue(QThread):
    # receive_debug_signal = pyqtSignal(np.ndarray)
    # debug_msgs = zss_debug_pb2.Debug_Msgs()
    def __init__(self):
        super().__init__()
        self._run_flag = False
        self._init_flag = True
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.sock.bind((ADDRESS.LOCAL_HOST, PORT.BLUE_DEBUG))
        mutex_blue.lock()

    def run(self):
        while self._run_flag:
            if self._init_flag == False:
                mutex_blue.lock()
            self.prodata, addr = self.sock.recvfrom(65535)
            if self._init_flag == False:
                self._init_flag = True
            mutex_blue.unlock()

    def restart(self):
        self._run_flag = True
        self.start()

    def stop(self):
        self._run_flag = False
        self.wait()

class UDPReceiveYellow(QThread):
    receive_debug_signal = pyqtSignal(np.ndarray)
    debug_msgs = zss_debug_pb2.Debug_Msgs()

    def __init__(self):
        super().__init__()
        self._run_flag = False
        self._init_flag = True
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.sock.bind((ADDRESS.LOCAL_HOST, PORT.YELLOW_DEBUG))
        mutex_yellow.lock()

    def run(self):
        while self._run_flag:
            if self._init_flag == False:
                mutex_yellow.lock()
            self.prodata, addr = self.sock.recvfrom(65535)
            if self._init_flag == False:
                self._init_flag = True
            mutex_yellow.unlock()

    def restart(self):
        self._run_flag = True
        self.start()

    def stop(self):
        self._run_flag = False
        self.wait()

class Blue_Update_Image(QThread):
    def __init__(self, win):
        super().__init__()
        self._run_flag = False
        self.win = win
        self.debug_msgs = zss_debug_pb2.Debug_Msgs()

    def run(self):
        while self._run_flag == True:
            update_one_frame(self, 1)

    def restart(self):
        self._run_flag = True
        self.start()

    def stop(self):
        if (mutex_blue.tryLock()):
            self._run_flag = False
            self.wait()
        mutex_blue.unlock()

class Yellow_Update_Image(QThread):
    def __init__(self, win):
        super().__init__()
        self._run_flag = False
        self.win = win
        self.debug_msgs = zss_debug_pb2.Debug_Msgs()

    def run(self):
        while self._run_flag == True:
            update_one_frame(self, 0)
    def restart(self):
        self._run_flag = True
        self.start()

    def stop(self):
        if (mutex_yellow.tryLock()):
            self._run_flag = False
            self.wait()
        mutex_yellow.unlock()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640 * 2
        self.display_height = 480 * 2
        self.setGeometry(0, 0, 1800, 900)
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
        self.image_label.setPixmap(QPixmap.fromImage(
            QImage('images/Sat Nov 25 17:43:20 2023.png').scaled(self.disply_width, self.display_height,
                                                                 Qt.AspectRatioMode.KeepAspectRatio)))
        self.label_blue_debug_msg = QLabel(self)
        self.label_blue_debug_msg.setGeometry(0, 0, 1500, 1500)

        self.label_yellow_debug_msg = QLabel(self)
        self.label_yellow_debug_msg.setGeometry(0, 0, 1500, 1500)

        self.label_visible = QLabel(self)
        self.label_visible.setStyleSheet("font-size: 30px;")
        self.label_visible.setText("Visible")
        self.label_visible.setGeometry(1240, 600, 100, 40)

        self.cmd_blue_debug_control = QPushButton(self)
        self.cmd_blue_debug_control.setIcon(QIcon("Icon/start2.png"))
        self.cmd_blue_debug_control.setText("Blue")
        self.cmd_blue_debug_control.setGeometry(1240, 500, 100, 20)
        self.cmd_blue_debug_control.clicked.connect(self.start_blue_receive)

        self.cmd_yellow_debug_control = QPushButton(self)
        self.cmd_yellow_debug_control.setIcon(QIcon("Icon/start2.png"))
        self.cmd_yellow_debug_control.setText("Yellow")
        self.cmd_yellow_debug_control.setGeometry(1240, 550, 100, 20)
        self.cmd_yellow_debug_control.clicked.connect(self.start_yellow_receive)

        self.cmd_quit = QPushButton("exit", self)
        self.cmd_quit.setGeometry(1240, 700, 100, 20)
        self.cmd_quit.clicked.connect(exit)

        self.checkbox_blue_debug_visible = QCheckBox(self)
        self.checkbox_blue_debug_visible.setText("Blue")
        self.checkbox_blue_debug_visible.setGeometry(1240, 630, 100, 20)
        self.checkbox_blue_debug_visible.setChecked(True)
        self.checkbox_blue_debug_visible.stateChanged.connect(self.set_visible)

        self.checkbox_yellow_debug_visible = QCheckBox(self)
        self.checkbox_yellow_debug_visible.setText("Yellow")
        self.checkbox_yellow_debug_visible.setGeometry(1240, 650, 100, 20)
        self.checkbox_yellow_debug_visible.setChecked(True)
        self.checkbox_yellow_debug_visible.stateChanged.connect(self.set_visible)

        self.pos1 = [0, 0]
        self.pos2 = [0, 0]

        self.blue_debug_thread = UDPReceiveBlue()
        self.blue_update_image_thread = Blue_Update_Image(self)
        self.yellow_debug_thread = UDPReceiveYellow()
        self.yellow_update_image_thread = Yellow_Update_Image(self)

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
        pen = QPen(COLOR.DEBUG[1], 5)  # red
        qp.setPen(pen)
        qp.drawLine(self.pos1[0], self.pos1[1], self.pos2[0], self.pos2[1])
        qp.end()
        self.label_board.setPixmap(pixmap)

    def start_blue_receive(self):
        self.blue_debug_thread.restart()
        self.blue_update_image_thread.restart()
        self.cmd_blue_debug_control.clicked.disconnect(self.start_blue_receive)
        self.cmd_blue_debug_control.clicked.connect(self.close_blue_receive)
        self.cmd_blue_debug_control.setIcon(QIcon("Icon/stop2.png"))

    def close_blue_receive(self):
        self.blue_debug_thread.stop()
        self.blue_update_image_thread.stop()
        self.cmd_blue_debug_control.clicked.disconnect(self.close_blue_receive)
        self.cmd_blue_debug_control.clicked.connect(self.start_blue_receive)
        self.cmd_blue_debug_control.setIcon(QIcon("Icon/start2.png"))

    def start_yellow_receive(self):
        self.yellow_debug_thread.restart()
        self.yellow_update_image_thread.restart()
        self.cmd_yellow_debug_control.clicked.disconnect(self.start_yellow_receive)
        self.cmd_yellow_debug_control.clicked.connect(self.close_yellow_receive)
        self.cmd_yellow_debug_control.setIcon(QIcon("Icon/stop2.png"))

    def close_yellow_receive(self):
        self.yellow_debug_thread.stop()
        self.yellow_update_image_thread.stop()
        self.cmd_yellow_debug_control.clicked.disconnect(self.close_yellow_receive)
        self.cmd_yellow_debug_control.clicked.connect(self.start_yellow_receive)
        self.cmd_yellow_debug_control.setIcon(QIcon("Icon/start2.png"))

    def set_visible(self):
        self.label_blue_debug_msg.setVisible(self.checkbox_blue_debug_visible.isChecked())
        self.label_yellow_debug_msg.setVisible(self.checkbox_yellow_debug_visible.isChecked())


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
