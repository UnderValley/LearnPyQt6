# Form implementation generated from reading ui file 'Event.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 250)
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(30, 160, 196, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(parent=Form)
        self.widget.setGeometry(QtCore.QRect(30, 30, 198, 60))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_click = QtWidgets.QPushButton(parent=self.widget)
        self.btn_click.setObjectName("btn_click")
        self.horizontalLayout.addWidget(self.btn_click)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.btn_click.clicked.connect(self.click_me)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def click_me(self):
        self.label.setText(self.lineEdit.text())

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Qt Designer Application"))
        self.label.setText(_translate("Form", "TextLabel"))
        self.btn_click.setText(_translate("Form", "Click ME"))
        self.lineEdit.setPlaceholderText(_translate("Form", "pls enter your name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
