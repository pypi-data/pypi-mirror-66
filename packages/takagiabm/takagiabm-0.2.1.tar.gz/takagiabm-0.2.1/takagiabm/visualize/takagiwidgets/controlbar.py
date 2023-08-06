from PyQt5.QtWidgets import QApplication, QMainWindow,  QToolBar, QAction, QComboBox
# from takagiabm.visualize.takagiwidgets.customizedwidgets.pushbutton import TakPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import takagiabm.visualize.takagiwidgets.colorutils as colorUtils
from takagiabm.visualize.takagiwidgets.customizedwidgets.label import TakLabel

from takagiabm.visualize.takagiwidgets.customizedwidgets.pushbutton import TakPushButton
from takagiabm.visualize.takagiwidgets.customizedwidgets.scrollbar import TakScrollBar
class TakControlBar(QToolBar):
    mainWindow = None

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.initBarWidgets()

    def singleStep(self):
        self.mainWindow.singleStep()
        self.pauseToolButton.setText("继续")

    def resetModel(self):
        self.mainWindow.resetModel()
        self.pauseToolButton.setText("开始")

    def setSpeed(self):
        self.mainWindow.setSpeed(self.speedControl.value())

    def pause(self):
        self.mainWindow.pause()  # 主窗口停止或者继续
        if (self.mainWindow.running == True):
            self.pauseToolButton.setText("暂停")
        else:
            self.pauseToolButton.setText("继续")

    def showSpeed(self, currentStep, speedDic):
        '''
         当前步数(int)，速度（dict）
        '''
        speedText = "当前步：%d, 设定步速：%.2f/s,实际帧率：%.2f/s,实际步速：%.2f/s" % (
            currentStep,
            speedDic['given'], speedDic['frames/s'], speedDic['steps/s'])
        self.showSpeedLabel.setText(speedText)

    def initBarWidgets(self):  # 初始化类、
        if (self.mainWindow == None):
            raise Exception("takagiwidgets.contolbar.ControlBar初始化时需要传入一QMainWindow作为参数。")
        self.restartToolButton = TakPushButton(QIcon(QPixmap("./image/wifi.png")), "重启", self)
        self.restartToolButton.clicked.connect(self.resetModel)
        self.stepToolButton = TakPushButton("单步", self)
        self.stepToolButton.clicked.connect(self.singleStep)

        self.pauseToolButton = TakPushButton(QIcon(QPixmap("./image/wifi.png")), "开始", self)
        self.pauseToolButton.clicked.connect(self.pause)

        self.speedControl = TakScrollBar(Qt.Horizontal)
        self.speedControl.setMaximum(2000)
        self.speedControl.setMinimum(1)
        self.speedControl.valueChanged.connect(self.setSpeed)

        self.speedControl.setMinimumWidth(250)
        self.addWidget(self.restartToolButton)
        self.addWidget(self.stepToolButton)
        self.addWidget(self.pauseToolButton)
        self.addWidget(self.speedControl)
        self.showSpeedLabel = TakLabel("")
        self.addWidget(self.showSpeedLabel)

        self.speedControl.setValue(20)
        self.setStyleSheet('''
        /*按钮普通态*/
QToolBar
{
    
    /*字体大小为20点*/
    font-size:20pt;
    /*字体颜色为白色*/    
    color:%s;
    /*背景颜色*/  
    background-color:%s;
    /*边框圆角半径为8像素*/ 
    border-radius:8px;
}
'''%(colorUtils.globalTextColor,colorUtils.globalBackgroundColor))


#         self.setStyleSheet('''
# /*按钮普通态*/
# QToolBar
# {
#     /*字体为微软雅黑*/
#     font-family:Microsoft Yahei;
#     /*字体大小为20点*/
#     font-size:20pt;
#     /*字体颜色为白色*/
#     color:white;
#     /*背景颜色*/
#     background-color:rgb(14 , 150 , 254);
#     /*边框圆角半径为8像素*/
#     border-radius:8px;
# }
# QAction:hover
# {
#     /*背景颜色*/
#     background-color:rgb(44 , 137 , 255);
# }
# ''')

'''
/*按钮停留态*/
QPushButton:hover
{
    /*背景颜色*/  
    background-color:rgb(44 , 137 , 255);
}

/*按钮按下态*/
QPushButton:pressed
{
    /*背景颜色*/  
    background-color:rgb(14 , 135 , 228);
    /*左内边距为3像素，让按下时字向右移动3像素*/  
    padding-left:3px;
    /*上内边距为3像素，让按下时字向下移动3像素*/  
    padding-top:3px;
        })
'''
