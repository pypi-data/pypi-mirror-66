'''
这个控件可以通过滑动来改变数值，进而改变行为模型参数。
'''
import sys
from PyQt5.QtWidgets import QHBoxLayout,QPushButton \
    , QApplication
from takagiabm.visualize.takagiwidgets.valuewidgets.basevaluewidget import TakBaseValueWidget
from takagiabm.visualize.takagiwidgets.customizedwidgets.label import TakLabel
from takagiabm.variable import TakVariable,Var
class TakValueButtonWidget(TakBaseValueWidget):
    min = 0
    max = 1
    step = 0
    name = ''
    accuracy = 2
    times = 0
    variable = None

    def __init__(self, var=None):
        super().__init__()
        self.name = var.name
        self.variable = var
        self.initWidget()
        self.setValue(var.value)


    def setVariable(self, var):
        self.variable = var


    def setName(self, name: str) -> None:
        if (type(name) == type('')):
            self.name = name
            self.nameLabel.setText(self.name)
        else:
            raise Exception("setName 方法必须输入字符串作为参数！ Method \"setName\" requires a string param.")

    def setupWidgets(self):

        self.valueWidget.setMinimumWidth(50)
        self.valueWidget.setText(repr(self.variable.value))
        self.nameLabel.setText(self.name)
        self.nameLabel.setMaximumWidth(100)
        self.valueWidget.clicked.connect(self.updateValue)

    def initWidget(self):
        layout = QHBoxLayout()
        self.valueWidget = QPushButton()
        self.nameLabel = TakLabel(self.name)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.valueWidget)

        self.setupWidgets()
        self.setLayout(layout)

    def updateValue(self):
        value=self.valueWidget.text()
        if(value=='False'):
            self.valueWidget.setText('True')
            self.variable.value=True
        else:

            self.valueWidget.setText('False')
            self.variable.value=False

        print(self.variable.value)

    def getValue(self):
        v = self.valueWidget.text()
        if(v=='True'):
            val=True
        else:
            val=False
        return val

    def setValue(self, value):
        self.valueWidget.setText(repr(value))
        self.variable.value=value


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tv= Var('hahahah',False)
    print(tv.value)
    ex = TakValueButtonWidget(tv)
    ex.show()
    sys.exit(app.exec_())