### coding= utf-8
##from PyQt5.QtCore import *
##from PyQt5.QtGui import *
##from PyQt5.QtWidgets import *
##
##
##import sys
##
##
##class ToolBar(QMainWindow):
##
##    def __init__(self):
##        super().__init__()
##        self._initUi()
##
##    def _initUi(self):
##        self.setWindowTitle("工具条实例")
##        # 获取当前屏幕分辨率
##        deskRect = QApplication.desktop().availableGeometry()  # type: QRect
##        mainWidth = 600
##        mainHeight = 400
##        self.setWindowFlags(Qt.Window) # 普通窗口
##        top = deskRect.height() // 2 - mainHeight / 2
##        left = deskRect.width() // 2 - mainWidth / 2
##        self.setGeometry(left, top, mainWidth, mainHeight) #居中
##        # 工具条
##        toolBar = QToolBar(self)
##        toolBar.setFixedHeight(24)
##        test1 = QPushButton("测试1")
##        test1.clicked.connect(self._tool_push1_clicked)
##        test2 = QPushButton("测试2")
##        test2.clicked.connect(self._tool_push2_clicked)
##        toolBar.addWidget(test1)
##        toolBar.addWidget(test2)
##        toolBar.setIconSize(QSize(16, 16))
##        toolBar.addAction( "Search" ,self._tool_search_)
##        self.addToolBar(Qt.TopToolBarArea, toolBar)
##
##        self.show()
##    def _tool_push1_clicked(self):
##        print("测试1被单击")
##    def _tool_push2_clicked(self):
##        ex = Example(self) #创建一个对话框
##        ex.exec_()#模态方式执行, show 为非模态
##    def _tool_search_(self):
##        print("出发search事件") #类似的快捷键， 工具条，菜单栏都会出发次事件
##
##if __name__ == "__main__":
##    app = QApplication(sys.argv)
##    ex = ToolBar()
##    sys.exit(app.exec_())
##
#理论上2和3版本都能用，对象能在多进程中共享传递，改变
from multiprocessing import Process, Value, Lock
from multiprocessing.managers import BaseManager
 
 
class Employee(object):
    def __init__(self, name, salary):
        self.name = name
        self.salary = Value('i', salary)
        self.data=[]
 
    def increase(self):
        self.salary.value += 100
        self.data.append(self.salary.value)
        print(self.data)
 
    def getPay(self):
        return self.name + ':' + str(self.salary.value)
 
 
class MyManager(BaseManager):
    pass
 
 
def Manager2():
    m = MyManager()
    m.start()
    return m
 
 
MyManager.register('Employee', Employee)
 
 
def func1(em, lock):
    with lock:
        em.increase()
 
 
if __name__ == '__main__':
    manager = Manager2()
    em = manager.Employee('zhangsan', 1000)
    lock = Lock()
    proces = [Process(target=func1, args=(em, lock)) for i in range(10)]
    for p in proces:
        p.start()
    for p in proces:
        p.join()
    print(em.getPay())