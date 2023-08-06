'''
这个文件中存储着用于控制的变量，它连接着变量控件，比如滚动条、选择开关等。

'''
import time
class TakVariable():
    def __init__(self):
        pass
        

class Var(TakVariable):# 可以是
    value=None# 可以是bool型(开关),数字型(滑动条),字符串型(文本输入框)
    valueWidget=None
    name=''
    def __init__(self,name='',value=None,range=(0,100,1)):
        super().__init__()
        self.name=name
        self.value=value
        if(type(value)==type(1))|(type(value)==type(1.0)):
            self.min=range[0]
            self.max=range[2]
            self.step=range[1]
        
        
    def setValueWidget(self,qWidget):# 可以是滑动条,也可以是其他的东西.
        self.valueWidget=qWidget
        # if (type(self.value) == type(1)) | type(self.value == type(1.0)):
        #     self.valueWidget.min=self.min
        #     self.valueWidget.max=self.max
        #     self.valueWidget.step=self.step
    def setName(self,name='unnamed'):
        self.name=name
        if self.valueWidget!=None:
            self.valueWidget.setName(name)
        
    def getValue(self):# 当其绑定的控件值改变时,自身value会改变.如果每次getvalue都要访问一下控件
        #,那么时间开销太大,得不偿失.
            
        return self.value
    def setValue(self,value)->None:
        self.value=value
        if(self.valueWidget!=None):
            self.valueWidget.setValue(value)
        
        