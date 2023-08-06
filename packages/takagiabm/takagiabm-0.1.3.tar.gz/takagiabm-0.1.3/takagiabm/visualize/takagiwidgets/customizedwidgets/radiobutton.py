from PyQt5.QtWidgets import QRadioButton
import takagiabm.visualize.takagiwidgets.colorutils as colorUtils
class TakRadioButton(QRadioButton):
    def __init__(self,*args):
        super().__init__(*args)
        self.setStyleSheet(
'''
QRadioButton {
    font-size: 12px;
    color: %s;
    font-family: %s;
    font-weight: bold;

    spacing: 5px;
    padding-left: 3px;
    padding-top: 0px;

    border-style: solid;
    border-width: 0.5px;
    border-color: %s;

    border-radius: 20;

    background-color: #2E3648;
    background-repeat: no-repeat;
    background-position: right center;
}''' % (colorUtils.globalTextColor,colorUtils.globalFont,colorUtils.globalBorderColor) + """
QRadioButton:hover{
	border-color: %s;
    background-color: %s;
}""" % (colorUtils.globalBorderColor, colorUtils.globalHoverBackgroundColor) )