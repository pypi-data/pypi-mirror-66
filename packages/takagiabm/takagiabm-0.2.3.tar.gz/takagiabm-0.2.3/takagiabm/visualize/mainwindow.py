from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget, QSplitter, QVBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtOpenGL import QGLWidget

import pyqtgraph as pg

from OpenGL.GL import *
from OpenGL.GLU import *
# from OpenGL.GLUT import *


import time
import numpy as np
import math
import os
from takagiabm.visualize.takagiwidgets.controlbar import TakControlBar
from takagiabm.visualize.takagiwidgets.menubar import takInitMenuBar
from takagiabm.visualize.takagiwidgets.valuewidgets.valuewidgetfactory import createValueWidget
from takagiabm.visualize.takagiwidgets.plotwidgets.plotwidgetfactory import createDataShowWidget
import takagiabm.visualize.takagiwidgets.colorutils as colorUtils
from takagiabm.toolbox.typeutils import ifColorArrEqual


class TakBaseWindow(QMainWindow):
    """这是主界面，由PyqtGraph和PyQt相结合写成。"""
    speed = {'frames/s': 0, 'given': 5, 'steps/s': 0, 'maxfps': 0}
    openGLWidget = None
    timeToUpdate = 0
    timeToThisStep = 0
    sourceFile = 0

    def __init__(self, sourceFile='', parent=None, modelClass=None, collectorList=[]):
        super(TakBaseWindow, self).__init__(parent)
        self.basic()
        # self.varList=varList
        self.modelClass = modelClass
        self.model = modelClass()
        self.sourceFile = sourceFile

        self.controlBar = TakControlBar(self)

        self.addToolBar(self.controlBar)

        takInitMenuBar(self)  # menuBar没有办法通过构造对象的方式获取，就只能这样弄了。
        self.running = False

        self.stepsPerFrame = 1
        self.stepToNextFrame = self.stepsPerFrame
        self.splitter_main = self.split_()
        self.setCentralWidget(self.splitter_main)
        self.s.setModel(self.model)

        self.refreshTimer = QtCore.QTimer()
        self.refreshTimer.timeout.connect(self.step)
        self.refreshTimer.start(1)

        self.UITimer = QtCore.QTimer()
        self.UITimer.timeout.connect(self.updateUI)

        self.UITimer.start(1000)
        self.setStyleSheet('QMainWindow{background-color:%s}' % colorUtils.globalBackgroundColor)  # 增加的代码
        self.setWindowIcon(QIcon(__file__.replace('mainwindow.py', 'hat.png')))

    def updateUI(self):
        self.showSpeed()

    def getRealSpeed(self):
        if (self.openGLWidget != None):
            interval = self.openGLWidget.updateInterval
            avgRefresh = self.openGLWidget.averageRefreshingTime
            #
            if (interval != 0) & (avgRefresh != 0):  # 防止除以0
                self.speed['frames/s'] = 1.0 / interval
                self.speed['maxfps'] = 1.0 / avgRefresh
            deltaStep = self.model.currentStep - self.model.lastStep
            self.model.lastStep = self.model.currentStep
            self.speed['steps/s'] = deltaStep

    def showSpeed(self):
        self.getRealSpeed()
        self.controlBar.showSpeed(self.model.currentStep, speedDic=self.speed)
        self.adjustSpeed()

    def adjustSpeed(self):
        '''
            根据当前刷新帧率以及输入的仿真速度，自动计算每次刷新对应的步数，并更新步数。
        '''
        if (self.speed['frames/s'] > 0):
            self.stepsPerFrame = round(1.0 * self.speed['given'] / self.speed['maxfps'])

    def setSpeed(self, speed):

        self.speed['given'] = speed

    def resetModel(self):
        import sys, traceback
        from imp import reload  # 要求：重新导入。

        (self.sourcePath, sourceFileName) = os.path.split(self.sourceFile)
        (moduleName, ext) = os.path.splitext(sourceFileName)
        sys.path.append(self.sourcePath)
        try:
            __import__(moduleName)
            if (moduleName in sys.modules.keys()):

                del sys.modules[moduleName]
                __import__(moduleName)
            else:
                __import__(moduleName)
            self.initControlPanel()  # 先初始化控制面板。因为控制面板可能会保存上次的输入。
            self.initViewPanel()
            self.model = self.modelClass()  # 重新初始化模型
            self.openGLWidget.setModel(self.model)  # 重新显示模型

            self.openGLWidget.bgColor = self.model.bgColor  # 设置背景颜色

            self.running = False
            self.visualize()
        except Exception as e:
            traceback.print_exc()

    def pause(self):
        if self.running:

            self.running = False
        else:
            self.running = True

    def basic(self):
        # 设置标题，大小，图标
        self.setWindowTitle("TakagiABM")
        self.setWindowIcon(QIcon("./image/TakagiABM.png"))
        # 居中显示
        screen = QDesktopWidget().geometry()
        self_size = self.geometry()
        self.resize(800, 500)
        self.move((screen.width() - self_size.width()) / 2, (screen.height() - self_size.height()) / 2)

    def initViewPanel(self):
        import sip
        print('count', self.viewLayout.count())
        # d = {}  # 用临时字典保存valueWidget上一次的值。

        for i in range(self.viewLayout.count() - 1, 0 - 1, -1):  # 删除。
            w = self.viewLayout.itemAt(i).widget()

            sip.delete(w)
            del w
        for cou in self.model.dataCounters:
            if type(cou) == type([]):
                pass
            else:
                print(cou)

                cdsw = createDataShowWidget(cou)
                self.viewLayout.addWidget(cdsw)

    def initControlPanel(self):
        import sip
        print('count', self.controlLayout.count())
        d = {}  # 用临时字典保存valueWidget上一次的值。

        for i in range(self.controlLayout.count() - 1, 0 - 1, -1):  # 删除。
            w = self.controlLayout.itemAt(i).widget()
            d[w.variable.name] = w.variable.value

            sip.delete(w)
            del w
        print(self.model.varList)
        for var in self.model.varList:
            if type(var) == type([]):
                pass
            else:
                print(var)

                tvsw = createValueWidget(var)  # TakValueScrollWidget(name=var.name)
                if (var.name in d.keys()):  # 如果相应的控件已经存在，就按照上一次的设定。
                    tvsw.setValue(d[var.name])
                self.controlLayout.addWidget(tvsw)

    def split_(self):
        splitter = QSplitter(Qt.Vertical)
        # s = self.s #将opengl例子嵌入GUI

        self.base = OpenGLBaseWidget()
        self.s = self.base.openGLWidget
        self.openGLWidget = self.s
        l = QVBoxLayout()
        l.addWidget(self.s)
        self.base.setLayout(l)

        self_size = self.base.geometry()

        splitter.addWidget(self.base)
        testedit = QTextEdit()
        self.controlPanel = QWidget()
        self.controlLayout = QVBoxLayout()
        self.controlPanel.setLayout(self.controlLayout)
        self.initControlPanel()

        splitter.addWidget(self.controlPanel)
        splitter.addWidget(testedit)
        splitter.setStretchFactor(0, 10)
        splitter.setStretchFactor(1, 1)

        screen = QDesktopWidget().geometry()

        splitter_main = QSplitter(Qt.Horizontal)
        textedit_main = pg.DataTreeWidget(data=None)
        splitter_main.addWidget(textedit_main)
        self.agentViewer = textedit_main

        splitter_main.addWidget(splitter)
        self.viewPanel = QWidget()
        self.viewLayout = QVBoxLayout()
        self.viewPanel.setLayout(self.viewLayout)
        self.initViewPanel()
        splitter_main.addWidget(self.viewPanel)

        splitter_main.setStretchFactor(0, 1)
        splitter_main.setStretchFactor(1, 3)
        splitter_main.setStretchFactor(2, 3)

        return splitter_main

    def visualize(self):
        self.openGLWidget.update()  # 刷新，生成网格。

    def singleStep(self):

        self.running = False

        self.model.step()
        self.visualize()

    def step(self):
        if not self.running:
            return
        t = time.time()
        if (t <= self.timeToThisStep):
            return
        self.model.step()
        if (self.stepToNextFrame <= 1):
            self.visualize()
            self.stepToNextFrame = self.stepsPerFrame
        else:
            self.stepToNextFrame -= 1
        self.timeToThisStep = t + 1.0 / self.speed['given']


class OpenGLBaseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.openGLWidget = OpenGLWidget()

    def resizeEvent(self, event):
        size = self.size()

        s = min([size.width(), size.height()])
        self.openGLWidget.resize(s, s)


class OpenGLWidget(QGLWidget):
    model = None
    refreshingTimeList = []
    refreshingTimeListLen = 10
    averageRefreshingTime = 0  # 刷新的平均时间
    lastUpdateTime = 0
    updateInterval = 0  # 两次刷新之间的时间间隔

    def __init__(self):
        self.gridScale = [1, 1]
        self.selectedGridPos = np.array([0, 0])
        self.lastEventPixPos = (0, 0)
        self.lastEventTime = time.time()
        super().__init__()
        self.setMouseTracking(False)
        self.bgcolor = [0, 0, 0]  # 背景为黑色的。

    def setModel(self, model):
        self.model = model

    def initializeGL(self):
        self.times = 0

        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)


        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)

    def mouse(self, *k):
        print(k)

    def mouseMoveEvent(self, event):  # 鼠标移动事件
        ret = self.hasMouseTracking()  # 返回鼠标MouseTracking的状态

        print(event.localPos(), event.x(), event.y(), event.windowPos(), event.globalX()
              , event.globalY())
        t = time.time()

        x0 = event.x() / self.width() * self.model.grid.width
        y0 = (self.height() - event.y()) / self.height() * self.model.grid.height
        self.selectedGridPos[0] = int(x0)
        self.selectedGridPos[1] = int(y0)
        print(self.model.grid.getAgentsByPos(np.array([int(y0), int(x0)])))
        if (int(x0) != self.lastEventPixPos[0]) | (int(y0) != self.lastEventPixPos[1]):  # |(t-self.lastEventTime>2):
            self.lastEventPixPos = (int(x0), int(y0))
        else:
            return
        for agent in self.model.grid.getAgentsByPos(np.array([int(x0), int(y0)])):
            agent.onClicked()
        self.model.grid.getCellByPos(np.array([int(x0), int(y0)], dtype=np.int)).onClicked()

        self.update()

    def mousePressEvent(self, event):
        print(event.localPos(), event.x(), event.y(), event.windowPos(), event.globalX()
              , event.globalY())
        x0 = event.x() / self.width() * self.model.grid.width
        y0 = (self.height() - event.y()) / self.height() * self.model.grid.height
        self.selectedGridPos[0] = int(x0)
        self.selectedGridPos[1] = int(y0)
        print(self.model.grid.getAgentsByPos(np.array([int(y0), int(x0)])))
        for agent in self.model.grid.getAgentsByPos(np.array([int(x0), int(y0)])):
            agent.onClicked()
        self.model.grid.getCellByPos(np.array([int(x0), int(y0)], dtype=np.int)).onClicked()
        self.update()

    def paintAgentsOnlyDot(self):
        glPointSize(5)
        glBegin(GL_POINTS)
        for agent in list(self.model.agentSet):
            x = agent.pos[0]
            y = agent.pos[1]
            color = agent.getColorArray(pos=np.array([x, y]))

            glColor3f(color[0], color[1], color[2])

            glVertex3f(x, y, 0)
        glEnd()

    def paintAgents(self):
        for agent in list(self.model.agentSet):
            glBegin(GL_POLYGON)
            x = agent.pos[0]
            y = agent.pos[1]
            color = agent.getColorArray(pos=np.array([x, y]))

            glColor3f(color[0], color[1], color[2])
            verts = agent.getVertArray()

            for val in verts:
                glVertex3f(x + val[0], y + val[1], 0)
            glEnd()

    def update(self):

        super().update()

    def calcRefreshTime(self, t1, t0):
        self.refreshingTimeList.append(t1 - t0)
        if (len(self.refreshingTimeList) >= self.refreshingTimeListLen):
            self.refreshingTimeList.pop(0)
        self.averageRefreshingTime = sum(self.refreshingTimeList) / len(self.refreshingTimeList) * 1.0

        self.updateInterval = t1 - self.lastUpdateTime
        self.lastUpdateTime = t1

    def paintCellHatch(self):
        width = self.model.grid.width
        height = self.model.grid.height
        w = self.gridScale[0]
        h = self.gridScale[1]
        mat = self.model.grid.colorList

        for x in range(width):
            for y in range(height):

                # time.time()
                color = mat[y][x]  #
                if ifColorArrEqual(color, self.bgcolor):
                    continue

                glColor3f(color[0], color[1], color[2])
                glRectf(x * w, y * h, (x + 1) * w, (y + 1) * h)  # 画矩形

    def resizeGL(self, w, h):
        # self.resize2(w,h)
        glViewport(0, 0, w, h);
        glLoadIdentity();

        glOrtho(0, self.model.grid.width * self.gridScale[0], 0.0, self.model.grid.height * self.gridScale[1]
                , 1.0, -1.0)

    def resize2(self, w, h):
        glViewport(0, 0, w, h);
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluPerspective(80.0, w / h, 0.1, 10000.0);

        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        gluLookAt(100.0, -100.0, 200.0, 100.0, 300.0, 0.0, 0.0, 1, 0.0);

    def paintGL(self):

        # 清除之前画面
        t0 = time.time()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.paintAgents()
        # self.paintAgentsOnlyDot()
        t1 = time.time()

        self.paintCellHatch()

        glFinish()
        self.adjustSize()

        self.calcRefreshTime(time.time(), t0)
        print('paintTime', time.time() - t0, time.time() - t1)  # ,time.time()-t2,t2-t1,t1-t0)

    def ChangeSize(w, h):
        global windowWidth, windowHeight
        if (h == 0):  # 防止除数为0
            h = 1
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if (w <= h):
            windowHeight = 250.0
            windowWidth = 250.0
        else:
            windowWidth = 250.0
            windowHeight = 250.0

        # 设置修剪窗口
        glOrtho(0.0, windowWidth, 0.0, windowHeight, 1.0, -1.0)

        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print('hahaha')
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
