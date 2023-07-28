# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\北醒资料\Benewake_WINCC\WINCC.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(452, 833)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\北醒资料\\Benewake_WINCC\\BenewakeLogo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 451, 91))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton_connect = QtWidgets.QPushButton(self.frame)
        self.pushButton_connect.setGeometry(QtCore.QRect(310, 8, 120, 28))
        self.pushButton_connect.setAutoRepeat(False)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.label_serial = QtWidgets.QLabel(self.frame)
        self.label_serial.setGeometry(QtCore.QRect(20, 15, 35, 16))
        self.label_serial.setObjectName("label_serial")
        self.comboBox_serial = QtWidgets.QComboBox(self.frame)
        self.comboBox_serial.setGeometry(QtCore.QRect(55, 12, 80, 21))
        self.comboBox_serial.setObjectName("comboBox_serial")
        self.label_baudrate = QtWidgets.QLabel(self.frame)
        self.label_baudrate.setGeometry(QtCore.QRect(145, 15, 50, 15))
        self.label_baudrate.setObjectName("label_baudrate")
        self.comboBox_baudrate = QtWidgets.QComboBox(self.frame)
        self.comboBox_baudrate.setGeometry(QtCore.QRect(210, 12, 80, 21))
        self.comboBox_baudrate.setObjectName("comboBox_baudrate")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(5, 65, 441, 41))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton_refresh = QtWidgets.QPushButton(self.frame)
        self.pushButton_refresh.setGeometry(QtCore.QRect(310, 45, 120, 28))
        self.pushButton_refresh.setObjectName("pushButton_refresh")
        self.label_id = QtWidgets.QLabel(self.frame)
        self.label_id.setGeometry(QtCore.QRect(145, 50, 65, 16))
        self.label_id.setObjectName("label_id")
        self.label_port = QtWidgets.QLabel(self.frame)
        self.label_port.setGeometry(QtCore.QRect(20, 50, 35, 15))
        self.label_port.setObjectName("label_port")
        self.comboBox_port = QtWidgets.QComboBox(self.frame)
        self.comboBox_port.setGeometry(QtCore.QRect(55, 47, 80, 21))
        self.comboBox_port.setObjectName("comboBox_port")
        self.comboBox_port.addItem("")
        self.comboBox_port.addItem("")
        self.comboBox_port.addItem("")
        self.comboBox_port.addItem("")
        self.lineEdit_id = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_id.setGeometry(QtCore.QRect(210, 48, 80, 21))
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(-1, 89, 451, 711))
        self.widget1.setObjectName("widget1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 452, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionChinese = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setUnderline(False)
        font.setKerning(False)
        self.actionChinese.setFont(font)
        self.actionChinese.setObjectName("actionChinese")
        self.actionEnglish = QtWidgets.QAction(MainWindow)
        self.actionEnglish.setObjectName("actionEnglish")
        self.menu.addAction(self.actionOpen)
        self.menu_2.addAction(self.actionChinese)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.actionEnglish)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        self.actionOpen.triggered.connect(MainWindow.trigger_actOpen) # type: ignore
        self.pushButton_connect.clicked.connect(MainWindow.connectSerial) # type: ignore
        self.pushButton_refresh.clicked.connect(MainWindow.refreshSerial) # type: ignore
        self.comboBox_port.currentIndexChanged['QString'].connect(MainWindow.comboBoxPortChange) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BW_WINCC"))
        self.pushButton_connect.setText(_translate("MainWindow", "连接串口"))
        self.label_serial.setText(_translate("MainWindow", "串口"))
        self.label_baudrate.setText(_translate("MainWindow", "波特率"))
        self.comboBox_baudrate.setItemText(0, _translate("MainWindow", "115200"))
        self.comboBox_baudrate.setItemText(1, _translate("MainWindow", "9600"))
        self.comboBox_baudrate.setItemText(2, _translate("MainWindow", "19200"))
        self.comboBox_baudrate.setItemText(3, _translate("MainWindow", "38400"))
        self.comboBox_baudrate.setItemText(4, _translate("MainWindow", "57600"))
        self.comboBox_baudrate.setItemText(5, _translate("MainWindow", "256000"))
        self.comboBox_baudrate.setItemText(6, _translate("MainWindow", "460800"))
        self.comboBox_baudrate.setItemText(7, _translate("MainWindow", "921600"))
        self.pushButton_refresh.setText(_translate("MainWindow", "刷新串口"))
        self.label_id.setText(_translate("MainWindow", "从机地址"))
        self.label_port.setText(_translate("MainWindow", "接口"))
        self.comboBox_port.setItemText(0, _translate("MainWindow", "UART"))
        self.comboBox_port.setItemText(1, _translate("MainWindow", "IIC"))
        self.comboBox_port.setItemText(2, _translate("MainWindow", "RS485"))
        self.comboBox_port.setItemText(3, _translate("MainWindow", "RS232"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "语言"))
        self.actionOpen.setText(_translate("MainWindow", "打开"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionChinese.setText(_translate("MainWindow", "中文"))
        self.actionEnglish.setText(_translate("MainWindow", "English"))
