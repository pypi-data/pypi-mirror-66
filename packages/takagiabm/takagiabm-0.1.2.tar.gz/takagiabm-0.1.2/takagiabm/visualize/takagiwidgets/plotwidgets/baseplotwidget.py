import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget, QPushButton, QHBoxLayout, \
    QRadioButton
from takagiabm.visualize.takagiwidgets.customizedwidgets.radiobutton import TakRadioButton
import pyqtgraph as pg
def takMakeColor(i,name=''):
    print(len(name))
    if(name.startswith('#'))&(len(name)==7):

        return pg.mkColor(name)
    return pg.intColor(i)
class TakBasePlotWidget(QWidget):
    def __init__(self, name='unnamed', updateInterval=500, dataCounter=None, displayLength=100,plotProperties={}):
        super().__init__()
        self.updateInterval = 500
        self.name = name
        self.plotProperties=plotProperties
        self.dataCounter = dataCounter
        btnLayout = QVBoxLayout()
        self.btn1 = TakRadioButton('显示全部')
        self.btn2 = TakRadioButton('显示一定长度')
        if (displayLength > 0):
            self.btn2.setChecked(True)
            self.displayLength = displayLength  # 最多画多少个点的数据、
            self.varToSave_displayLength = displayLength  # 这个是用来储存self.displayLength的。当displayLength被修改的时候，
            # self.varToSave_displayLength不会被修改。用在图像显示的模式选择中。
        else:
            self.btn1.setChecked(True)
            self.displayLength = displayLength
            self.varToSave_displayLength = 100  # 至少显示100个点吧。

        self.btn1.toggled.connect(lambda: self.radioButtonEvent(self.btn1))
        self.btn1.toggled.connect(lambda: self.radioButtonEvent(self.btn2))
        btnLayout.addWidget(self.btn1)
        btnLayout.addWidget(self.btn2)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(btnLayout)
        self.canvas=None
        self.initCanvas()# 指定对应的画布对象。
        self.canvas.updateInterval = self.updateInterval
        self.mainLayout.addWidget(self.canvas)
        self.setLayout(self.mainLayout)

    def initCanvas(self):
        self.canvas = PlotCanvas(self, width=5, height=4)  # 实例化一个画布对象



    def radioButtonEvent(self, button):
        if (self.btn1.isChecked() == True):
            self.displayLength = 0
            self.canvas.displayLength = self.displayLength
        if (self.btn2.isChecked() == True):
            self.displayLength = self.varToSave_displayLength
            self.canvas.displayLength = self.displayLength

    def plot(self, dataDic):
        self.canvas.updateFigure(dataDic=dataDic)
    def calcStrTakValue(self,color:str):# Tak值是一个将字符串变成分立颜色值的算法。目的是强调首尾数位。
        # np.fromstring
        pen = (217, 83, 25)

if __name__ == '__main__':
    class App(QMainWindow):

        def __init__(self):
            super().__init__()
            self.left = 10
            self.top = 10
            self.title = '这里可以修改标题'
            self.width = 640
            self.height = 400
            self.initUI()

        def initUI(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)

            self.mplPlotWidget = TakBasePlotWidget()
            self.setCentralWidget(self.mplPlotWidget)

            button = QPushButton('这是一个按钮', self)
            button.setToolTip('This s an example button')
            button.move(500, 0)
            button.resize(140, 100)
            button.clicked.connect(self.mplPlotWidget.canvas.plot)

            self.show()



    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
