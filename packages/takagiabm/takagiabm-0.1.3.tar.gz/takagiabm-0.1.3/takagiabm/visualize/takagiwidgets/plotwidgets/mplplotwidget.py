import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget, QPushButton, QHBoxLayout, \
    QRadioButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt5.QtCore import QTimer
import random
import numpy as np
from takagiabm.visualize.takagiwidgets.plotwidgets.baseplotwidget import TakBasePlotWidget


class TakMPLPlotWidget(TakBasePlotWidget):
    def __init__(self, name='unnamed', updateInterval=500, dataCounter=None, displayLength=100):
        super().__init__(name=name, updateInterval=updateInterval, dataCounter=dataCounter, displayLength=displayLength)

    def initCanvas(self):
        self.canvas = PlotCanvas(self, width=5, height=4)

    def plot(self, dataDic):
        self.canvas.updateFigure(dataDic=dataDic)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100, displayLength=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.parent = parent
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.init_plot()#打开App时可以初始化图片
        self.displayLength = displayLength

    def plot(self, dataDic={'': np.linspace(1, 2, 100)}):
        dataDic = {'dd': np.linspace(1, 2, 100)}
        self.updateFigure(dataDic=dataDic)

    def foo(self):
        pass

    def init_plot(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
        self.axes.plot(x, y)

    def updateFigure(self, dataDic={'': np.linspace(1, 2, 100)}):
        t0 = time.time()
        self.axes.cla()

        dataLength = len(dataDic['_steps'])
        for k in dataDic.keys():
            if (k != '_steps'):
                if (self.displayLength > 0):
                    x = dataDic['_steps'][dataLength - self.displayLength:dataLength]
                    y = dataDic[k][dataLength - self.displayLength:dataLength]
                else:
                    x = dataDic['_steps']
                    y = dataDic[k]
                if (k == ''):
                    name = 'num'
                else:
                    name = k
                self.axes.plot(x, y, '-', label=name)
        self.axes.legend()

        self.axes.set_xlabel('hh')
        self.axes.set_title(self.parent.name)
        t1 = time.time()
        print(t1 - t0)
        self.draw()

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

            self.mplPlotWidget = TakMPLPlotWidget()
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
