from PyQt5.QtWidgets import QLabel
import takagiabm.visualize.takagiwidgets.colorutils as colorUtils
class TakLabel(QLabel):
    def __init__(self,*args):
        super().__init__(*args)
        self.setStyleSheet(
'''
QLabel { background-color: %s; 
color:%s;
}
'''%(colorUtils.globalBackgroundColor,colorUtils.globalTextColor)
        )