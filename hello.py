import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Uitestqt import Ui_MainWindow

# 导入 Ui_testqt.py 中的 Ui_MainWindow 界面类

class MyMainWindow(QMainWindow, Ui_MainWindow):  # 继承 QMainWindow类和 Ui_MainWindow界面类
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类

    def click_pushButton_2(self):  # 点击 pushButton_2 触发
        self.lineEdit_2.setText("click_pushButton_2")
        return
    
    def click_pushButton_3(self):  # 点击 pushButton_3 触发
        from datetime import datetime  # 导入 datetime 库
        nowDate = datetime.now().strftime("%Y-%m-%d")  # 获取当前日期 "2021-10-10"
        nowTime = datetime.now().strftime("%H:%M:%S")  # 获取当前时间 "16:58:00"
        self.lineEdit.setText("Current date: {}".format(nowDate))  # 显示日期
        self.lineEdit_2.setText("Current time: {}".format(nowTime))  # 显示时间
        self.lineEdit_3.setText("Demo4 of GUI by PyQt5")  #
        return

    def trigger_actHelp(self):  # 动作 actHelp 触发
        QMessageBox.about(self, "About",
                          """数字图像处理工具箱 v1.0\nCopyright YouCans, XUPT 2021""")
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    myWin = MyMainWindow()  # 实例化 MyMainWindow 类，创建主窗口
    myWin.show()  # 在桌面显示控件 myWin
    #MainWindow = QMainWindow()  # 创建主窗口
    #ui = Ui_testqt.Ui_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()  # 创建主窗口
    sys.exit(app.exec_())  # 在主线程中退出
