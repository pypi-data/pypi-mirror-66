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
import pyqtgraph.widgets.RemoteGraphicsView

class TakPGPlotWidget(TakBasePlotWidget):
    def __init__(self,name='unnamed',updateInterval=500,dataCounter=None,displayLength=100):
        super().__init__(name=name,updateInterval=updateInterval,dataCounter=dataCounter,displayLength=displayLength)
    def initCanvas(self):
        self.canvas=TakPGPlotCanvasWidget(self)

    def plot(self,dataDic,figureTitle=''):
        self.canvas.updateFigure(dataDic,figureTitle=figureTitle)

    def plotTest(self):
        dataDic = {'': np.linspace(1, 2, 1000), '_steps': np.random.random(100)}
        self.canvas.updateFigure(dataDic, figureTitle="figureTitle")

class TakPGRemotePlotCanvasWidget(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent=parent
        # self.pg.setConfigOptions(antialias=True)
        self.view=pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
        # self.plotItem = self.view.getPlotItem()

    def updateFigure(self,dataDic={},figureTitle=''):
        self.plotItem._setProxyOptions(deferGetattr=True)
        self.setCentralItem(self.plotItem)
        self.plotItem.plot(dataDic['_steps'],dataDic[''],clear=True,_callSync='off')

class TakPGPlotCanvasWidget(PlotWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent=parent
        self.displayLength=parent.displayLength
        self.colorIntDic={}
        self.setBackground(None)
        self.legend=self.addLegend()
    def updateFigure(self, dataDic={'':np.linspace(1,2,1000),'_steps':np.random.random(100)},figureTitle=''):
        t0=time.time()
        dataLength=len(dataDic['_steps'])
        # print(self.legend)
        for k in dataDic.keys():
            if(k!='_steps'):
                if(self.displayLength>0):
                    x = dataDic['_steps'][dataLength-self.displayLength:dataLength]
                    y = dataDic[k][dataLength-self.displayLength:dataLength]
                else:
                    x=dataDic['_steps']
                    y=dataDic[k]
                if(k==''):
                    name='num'
                else:
                    name=k
                if(name in self.colorIntDic):
                   self.colorIntDic[name][0].setData(x,y)
                else:
                    color=takMakeColor(len(self.colorIntDic),name=name)
                    curve=self.plot(x, y, pen=color, name=name)
                    self.colorIntDic[name]=[curve]
        self.showGrid(x=True, y=True)
        self.setLabel(axis="left", text="值")
        self.setLabel(axis="bottom", text="步数 / 步")
        # print('name',self.name)
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
            # self.view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
            # self.plotItem=self.view.pg.plotItem()
        def initUI(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)

            self.mplPlotWidget=TakPGPlotWidget()
            self.setCentralWidget(self.mplPlotWidget)

            button = QPushButton('这是一个按钮', self)
            button.setToolTip('This s an example button')
            button.move(500, 0)
            button.resize(140, 100)
            button.clicked.connect(self.mplPlotWidget.plotTest)

            self.show()
    app = pg.mkQApp()

    # a = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
    # pg.setConfigOptions(antialias=True)  ## this will be expensive for the local plot
    # layout = pg.LayoutWidget()
    # layout.addWidget(a, row=1, col=0, colspan=3)
    # layout.show()
    # a.pg.plotItem()

    ex = App()
    sys.exit(app.exec_())

