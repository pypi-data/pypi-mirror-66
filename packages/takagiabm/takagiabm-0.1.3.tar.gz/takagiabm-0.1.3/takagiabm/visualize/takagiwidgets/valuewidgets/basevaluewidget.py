'''
这个控件可以通过滑动来改变数值，进而改变行为模型参数。
'''
import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout \
    , QApplication
from takagiabm.visualize.takagiwidgets.customizedwidgets.pushbutton import TakPushButton
from takagiabm.visualize.takagiwidgets.customizedwidgets.label import TakLabel
from PyQt5.QtCore import Qt


class TakBaseValueWidget(QWidget):
    name = ''
    variable = None
    nameLabel=None
    valueLabel=None
    valueWidget=None
    def __init__(self, name='unnamed', var=None):
        super().__init__()
        self.name=name
        self.variable=var

    def setVariable(self, var):
        self.variable = var

    def reset(self, var=None):

        self.setupWidgets()
        self.setValue(var.value)
        self.setVariable(var)

    def setName(self, name: str) -> None:
        if (type(name) == type('')):
            self.name = name
            self.nameLabel.setText(self.name)
        else:
            raise Exception("setName 方法必须输入字符串作为参数！ Method \"setName\" requires a string param.")

    def setupWidgets(self):
        pass

    def initWidget(self):
        self.nameLabel = TakLabel(self.name)
        self.valueLabel = TakPushButton()
        self.layout = QHBoxLayout()

    def updateValue(self):
        v = self.scrollBar.value()
        val = v * self.step + self.min
        self.valueLabel.setText("%f" % (val))
        if (self.variable != None):
            self.variable.value = val

    def getValue(self):
        v = self.scrollBar.value()

        return v * self.step + self.min

    def setValue(self, value):
        self.scrollBar.setValue(int((value - self.min) / self.step))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TakBaseValueWidget("当前速度是", 0)
    ex.show()
    sys.exit(app.exec_())