# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\00_Practice\02_Project\04_UpperComputer\BW_TFSET_PY_GUI\WINCC.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(701, 879)
        MainWindow.setMinimumSize(QtCore.QSize(550, 200))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\00_Practice\\02_Project\\04_UpperComputer\\BW_TFSET_PY_GUI\\BenewakeLogo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(10, 110, 681, 741))
        self.widget1.setObjectName("widget1")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 701, 121))
        self.frame.setMinimumSize(QtCore.QSize(550, 110))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_connect = QtWidgets.QPushButton(self.frame)
        self.pushButton_connect.setAutoRepeat(False)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.gridLayout.addWidget(self.pushButton_connect, 0, 6, 1, 1)
        self.lineEdit_id = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.gridLayout.addWidget(self.lineEdit_id, 1, 4, 1, 1)
        self.comboBox_port = QtWidgets.QComboBox(self.frame)
        self.comboBox_port.setObjectName("comboBox_port")
        self.comboBox_port.addItem("")
        self.comboBox_port.addItem("")
        self.comboBox_port.addItem("")
        self.comboBox_port.addItem("")
        self.gridLayout.addWidget(self.comboBox_port, 1, 1, 1, 1)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 7)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_port = QtWidgets.QLabel(self.frame)
        self.label_port.setObjectName("label_port")
        self.gridLayout.addWidget(self.label_port, 1, 0, 1, 1)
        self.comboBox_serial = QtWidgets.QComboBox(self.frame)
        self.comboBox_serial.setObjectName("comboBox_serial")
        self.gridLayout.addWidget(self.comboBox_serial, 0, 1, 1, 1)
        self.comboBox_baudrate = QtWidgets.QComboBox(self.frame)
        self.comboBox_baudrate.setObjectName("comboBox_baudrate")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.gridLayout.addWidget(self.comboBox_baudrate, 0, 4, 1, 1)
        self.label_id = QtWidgets.QLabel(self.frame)
        self.label_id.setObjectName("label_id")
        self.gridLayout.addWidget(self.label_id, 1, 3, 1, 1)
        self.label_serial = QtWidgets.QLabel(self.frame)
        self.label_serial.setObjectName("label_serial")
        self.gridLayout.addWidget(self.label_serial, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.pushButton_refresh = QtWidgets.QPushButton(self.frame)
        self.pushButton_refresh.setObjectName("pushButton_refresh")
        self.gridLayout.addWidget(self.pushButton_refresh, 1, 6, 1, 1)
        self.label_baudrate = QtWidgets.QLabel(self.frame)
        self.label_baudrate.setObjectName("label_baudrate")
        self.gridLayout.addWidget(self.label_baudrate, 0, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 5, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 5, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 701, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menubangzhu = QtWidgets.QMenu(self.menubar)
        self.menubangzhu.setObjectName("menubangzhu")
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
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menu.addAction(self.actionOpen)
        self.menu_2.addAction(self.actionChinese)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.actionEnglish)
        self.menubangzhu.addAction(self.actionHelp)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menubangzhu.menuAction())

        self.retranslateUi(MainWindow)
        self.actionOpen.triggered.connect(MainWindow.trigger_actOpen) # type: ignore
        self.pushButton_refresh.clicked.connect(MainWindow.refreshSerial) # type: ignore
        self.pushButton_connect.clicked.connect(MainWindow.connectSerial) # type: ignore
        self.comboBox_port.currentIndexChanged['QString'].connect(MainWindow.comboBoxPortChange) # type: ignore
        self.actionHelp.triggered.connect(MainWindow.trigger_actHelp) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BW_WINCC_V1.1.1"))
        self.pushButton_connect.setText(_translate("MainWindow", "连接串口"))
        self.comboBox_port.setItemText(0, _translate("MainWindow", "UART"))
        self.comboBox_port.setItemText(1, _translate("MainWindow", "IIC"))
        self.comboBox_port.setItemText(2, _translate("MainWindow", "RS485"))
        self.comboBox_port.setItemText(3, _translate("MainWindow", "RS232"))
        self.label_port.setText(_translate("MainWindow", "接口"))
        self.comboBox_baudrate.setItemText(0, _translate("MainWindow", "115200"))
        self.comboBox_baudrate.setItemText(1, _translate("MainWindow", "9600"))
        self.comboBox_baudrate.setItemText(2, _translate("MainWindow", "19200"))
        self.comboBox_baudrate.setItemText(3, _translate("MainWindow", "38400"))
        self.comboBox_baudrate.setItemText(4, _translate("MainWindow", "57600"))
        self.comboBox_baudrate.setItemText(5, _translate("MainWindow", "256000"))
        self.comboBox_baudrate.setItemText(6, _translate("MainWindow", "460800"))
        self.comboBox_baudrate.setItemText(7, _translate("MainWindow", "921600"))
        self.label_id.setText(_translate("MainWindow", "从机地址"))
        self.label_serial.setText(_translate("MainWindow", "串口"))
        self.pushButton_refresh.setText(_translate("MainWindow", "刷新串口"))
        self.label_baudrate.setText(_translate("MainWindow", "波特率"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "语言"))
        self.menubangzhu.setTitle(_translate("MainWindow", "帮助"))
        self.actionOpen.setText(_translate("MainWindow", "打开"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionChinese.setText(_translate("MainWindow", "中文"))
        self.actionEnglish.setText(_translate("MainWindow", "English"))
        self.actionHelp.setText(_translate("MainWindow", "文档"))
        self.actionHelp.setShortcut(_translate("MainWindow", "Ctrl+H"))
