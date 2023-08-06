from takagiabm.visualize.takagiwidgets.valuewidgets.valuescrollwidget import TakValueScrollWidget
from takagiabm.visualize.takagiwidgets.valuewidgets.valuebuttonwidget import TakValueButtonWidget

def createValueWidget(var,widgetClassName=""):
    '''
    对于整数,返回滑动条来进行设置.widgetClassName是控件类的名字,可以输入spinbox输入可以作为另一个参数.
    '''
    if(type(var.value)==type(1.0))|(type(var.value)==type(1)):
        if(widgetClassName.lower()!="spinbox"):
            t=TakValueScrollWidget(name=var.name,var=var,max=var.max,min=var.min,step=var.step)
            # t.setVariable(var)
            return t
        else:
            pass
    elif(type(var.value)==type(False)):
        t=TakValueButtonWidget(var=var)
        return t
    
