import sys
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton
import numpy as np
# from takagiabm.visualize.takagiwidgets.plotwidgets.baseplotwidget import  TakBasePlotWidget,takMakeColor
from takagiabm.visualize.takagiwidgets.anime.baseanimewidget import TakBaseAnimeWidget
import pyqtgraph as pg

import pyqtgraph.widgets.RemoteGraphicsView

from takagiabm.agents.vehicle_station.vehicles import Vehicle
class TakPGAnimeWidget(TakBaseAnimeWidget):
    def __init__(self, name='unnamed', updateInterval=500, dataCounter=None, displayLength=100):
        super().__init__(name=name, updateInterval=updateInterval, dataCounter=dataCounter, displayLength=displayLength)

    def initCanvas(self):
        self.canvas = TakPGPlotCanvasWidget(self)

    def plot(self, dataDic, figureTitle=''):
        self.canvas.updateFigure(dataDic, figureTitle=figureTitle)

    def plotTest(self):
        dataDic = {'': np.linspace(1, 2, 1000), '_steps': np.random.random(100)}
        self.canvas.updateFigure(dataDic, figureTitle="figureTitle")


# class TakPGRemotePlotCanvasWidget(QWidget):
#     def __init__(self, parent):
#         super().__init__()
#         self.parent = parent
#         self.view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
#
#
#     def updateFigure(self, dataDic={}, figureTitle=''):
#         self.plotItem._setProxyOptions(deferGetattr=True)
#         self.setCentralItem(self.plotItem)
#         self.plotItem.plot(dataDic['_steps'], dataDic[''], clear=True, _callSync='off')




class Station():
    def __init__(self, pos=np.array([0, 0])):
        self.pos = pos

        self.properties = {}




class TakPGPlotCanvasWidget(pg.GraphicsLayoutWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.displayLength = parent.displayLength
        self.colorIntDic = {}
        self.setBackground(None)
        self.viewBox = self.addViewBox()
        x = np.r_[np.linspace(0, 100, 100), np.linspace(100, 100, 100)]
        y = np.r_[np.linspace(0, 0, 100), np.linspace(0, 100, 100)]
        self.x = x
        self.y = y

        self.plotItem = pg.PlotItem()
        curve = self.plotItem.plot(x, y)
        self.viewBox.addItem(curve)


        self.curvePoint = pg.CurvePoint(curve)

        self.viewBox.addItem(self.curvePoint)
        vehicle=Vehicle(0,1,self.curvePoint)

        self.textList=[]
        self.arrowList=[]
        self.vehicleList=[]
        self.routeList=[]
        self.addVehicle(vehicle,self.curvePoint)

        self.curvePoint2 = pg.CurvePoint(curve)

        vehicle2=Vehicle(180,-1,self.curvePoint2)
        vehicle2.text='gggg'
        self.addVehicle(vehicle2,self.curvePoint2)

        # self.v=VehicleVisualItem(self.viewBox,v,self.curvePoint2)
        self.index = 0

        # self.graphItem = pg.GraphItem()

        # self.viewBox.addItem(self.graphItem)
        pos = np.array([[1, 2], [3, 4]])
        # self.graphItem.setData(pos=pos, pxMode=False, size=3,
        #                        symbol='s')  # symbols = ['o','o','o','o','t','+'],pxMode=False
        # self.graphItem.setParentItem(self.curvePoint)  # 直接被曲线上的点拖着走。
        # self.vehicleList = []
        self.i = 0
    def addVehicle(self,vehicle,route):


        self.textList.append( pg.TextItem("test%s"%vehicle.text, anchor=(0.5, -1.0)))

        self.textList[len(self.textList)-1].setParentItem(route)
        arrow=pg.ArrowItem(angle=vehicle.heading)
        arrow.setParentItem(route)
        self.arrowList.append(arrow)

        self.vehicleList.append(vehicle)
        self.routeList.append(route)
    def removeVehicle(self,vehicle):# 不用从画布中移除。一旦失去外部引用，它就不会显示，然后等着gc让它自生自灭就行了。
        i=self.vehicleList.index(vehicle)
        self.vehicleList.pop(i)
        self.arrowList.pop(i)
        self.textList.pop(i)
        c=self.routeList.pop(i)
        self.viewBox.removeItem(c)
    def updateFigure(self, dataDic={'': np.linspace(1, 2, 1000), '_steps': np.random.random(100)}, figureTitle=''):
        # print(self.i)
        self.i += 1
        t0 = time.time()
        self.index = (self.index + 1) % len(self.x)
        for i,v in enumerate(self.vehicleList):
            v.step()
            self.routeList[i].setPos(self.vehicleList[i].pos1d*1.0/len(self.x))

        # self.curvePoint.setPos(self.vehicleList[0].pos1d*1.0/len(self.x))
        #
        # self.curvePoint2.setPos(self.vehicleList[1].pos1d*1.0/len(self.x))
        # self.curvePoint.setPos(self.index/len(self.x))
        if(len(self.vehicleList)>1):
            if(self.vehicleList[1].pos1d<100):
                self.removeVehicle(self.vehicleList[1])
        # print(self.index,self.vehicleList[0].pos1d,self.vehicleList[1].pos1d)
        t1 = time.time()
        print(t1 - t0)


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
            # self.view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
            # self.plotItem=self.view.pg.plotItem()

        def initUI(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)

            self.mplPlotWidget = TakPGAnimeWidget()
            self.setCentralWidget(self.mplPlotWidget)

            button = QPushButton('这是一个按钮', self)
            button.setToolTip('This s an example button')
            button.move(250, 0)
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
    timer = QTimer()
    timer.timeout.connect(ex.mplPlotWidget.plotTest)
    timer.start(10)

    sys.exit(app.exec_())
