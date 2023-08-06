from PyQt5.QtWidgets import QPushButton
import takagiabm.visualize.takagiwidgets.colorutils as colorUtils
# import takagiabm.visualize.takagiwidgets.colorutils
class TakPushButton(QPushButton):
    def __init__(self,*args):
        super().__init__(*args)
        self.setStyleSheet(
'''
QPushButton { background-color: %s; 
color:%s;
}
'''%(colorUtils.globalBackgroundColor,colorUtils.globalTextColor)
        )