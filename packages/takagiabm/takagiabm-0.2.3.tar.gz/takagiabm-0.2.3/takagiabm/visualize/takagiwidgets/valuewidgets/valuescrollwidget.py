'''
这个控件可以通过滑动来改变数值，进而改变行为模型参数。
'''
import sys
from PyQt5.QtWidgets import QHBoxLayout\
,QApplication
from PyQt5.QtCore import Qt
from takagiabm.visualize.takagiwidgets.valuewidgets.basevaluewidget import TakBaseValueWidget
from takagiabm.visualize.takagiwidgets.customizedwidgets.label import TakLabel
from takagiabm.visualize.takagiwidgets.customizedwidgets.scrollbar import TakScrollBar
class TakValueScrollWidget(TakBaseValueWidget):
    min=0
    max=1
    step=0
    name=''
    accuracy=2
    times=0
    variable=None
    def __init__(self,name='unnamed',min=0,max=100,value=20,step=1,var=None):
        super().__init__(name=name,var=var)
        self.max=max
        self.min=min
        self.step=step
        self.initWidget()
        self.setValue(var.value)

    def setupWidgets(self):
        self.scrollBar.setMaximum(int((self.max-self.min)/self.step+1))
        self.scrollBar.setMinimum(0)
        self.scrollBar.setMinimumWidth(100)
        self.nameLabel.setText(self.name)
        self.nameLabel.setMaximumWidth(100)
        self.valueLabel.setMaximumWidth(80)
        self.minShowLabel.setMaximumWidth(50)
        self.maxShowLabel.setMaximumWidth(50)
        self.minShowLabel.setText(str(self.min))
        self.maxShowLabel.setText(str(self.max))
        self.scrollBar.valueChanged.connect(self.updateValue) 
    def initWidget(self):
        layout=QHBoxLayout()
        self.scrollBar=TakScrollBar(Qt.Horizontal)
        paramTmp=1/self.step

        self.nameLabel=TakLabel(self.name)
        self.valueLabel=TakLabel()
        self.minShowLabel=TakLabel()
        self.maxShowLabel=TakLabel(str(self.max))

        layout.addWidget(self.nameLabel)
        layout.addWidget(self.minShowLabel)
        layout.addWidget(self.scrollBar)
        layout.addWidget(self.maxShowLabel)
        layout.addWidget(self.valueLabel)
        
        self.setupWidgets()
        self.setLayout(layout) 
         
         
    def updateValue(self):
        v=self.scrollBar.value()
        val=v*self.step+self.min
        self.valueLabel.setText("%f"%(val))
        if(self.variable!=None):
            self.variable.value=val
        
    def getValue(self):
        v=self.scrollBar.value()
        
        return v*self.step+self.min
    def setValue(self,value):
        self.scrollBar.setValue(int((value-self.min)/self.step))
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = TakValueScrollWidget("当前速度是",0,1001,407.1,0.3)
    ex.show()
    sys.exit(app.exec_())