'''
下一步是将这个widget放进单元工厂中，就可以了！
然后再测试一下收集多属性的能力！

'''
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow,QVBoxLayout, QSizePolicy, QWidget,QPushButton,QHBoxLayout,QRadioButton
from pyqtgraph import PlotWidget
import numpy as np
from takagiabm.visualize.takagiwidgets.plotwidgets.baseplotwidget import  TakBasePlotWidget,takMakeColor
import pyqtgraph as pg

class TakPGBarPlotWidget(TakBasePlotWidget):
    def __init__(self,name='unnamed',updateInterval=500,dataCounter=None,displayLength=100):
        super().__init__(name=name,updateInterval=updateInterval,dataCounter=dataCounter,displayLength=displayLength)
    def initCanvas(self):
        self.canvas=TakPGPlotCanvasWidget(self)


    def plot(self,dataDic,figureTitle=''):
        self.canvas.updateFigure(dataDic,figureTitle=figureTitle)
    def plotTest(self):
        dataDic = {'hhh': 123, 'fff': 4456}
        self.plot(dataDic)


class TakPGPlotCanvasWidget(PlotWidget):# 这个需要一定的PyQt的基础绘图知识。

    def __init__(self, parent=None):
        super().__init__()
        self.parent=parent
        self.displayLength=parent.displayLength
        self.colorIntDic={}
        self.setBackground(None)
        self.legend=self.addLegend()
        self.tickList = [[], []]

    def updateFigure(self, dataDic={'ggg':23,'_sfteps':40},figureTitle=''):
        t0=time.time()
        x = np.arange(10)
        self.showGrid(x=True, y=True)
        self.setLabel(axis="left", text="值")
        self.setLabel(axis="bottom", text="步数 / 步")
        self.setTitle(figureTitle)
        self.plotItem.clear()
        # self.plotItem.getAxis().
        for x,k in enumerate(dataDic.keys()):
            if(k!='_steps'):
                if(k==''):
                    name='num'
                else:
                    name=k
                if(k in self.colorIntDic.keys()):

                    bar = pg.BarGraphItem(x=[x], height=[dataDic[k]], width=0.3, brush=self.colorIntDic[k][1], name='ddddd')
                    self.addItem(bar)
                    self.tickList[0].append([x,name])
                else:
                    order=len(self.colorIntDic)# 序号
                    color=takMakeColor(order,name)
                    bar=pg.BarGraphItem(x=[x], height=[dataDic[k]], width=0.3, brush=color,name='ddddd')
                    self.colorIntDic[k]=[order,color,bar]
                    self.addItem(bar)
                    a = self.plotItem.getAxis('bottom')
                    a.setTicks(self.tickList)

        self.setTitle(figureTitle)
        t1=time.time()

        print(t1-t0)
if __name__=='__main__':
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

            self.mplPlotWidget=TakPGBarPlotWidget()
            self.setCentralWidget(self.mplPlotWidget)

            button = QPushButton('这是一个按钮', self)
            button.setToolTip('This s an example button')
            button.move(500, 0)
            button.resize(140, 100)
            button.clicked.connect(self.mplPlotWidget.plotTest)

            self.show()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

