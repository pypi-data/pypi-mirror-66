
# from takagiabm.visualize.takagiwidgets.plotwidgets.mplplotwidget import TakMPLPlotWidget不能使用！！！放弃mpl吧！
from takagiabm.visualize.takagiwidgets.plotwidgets.pgplotwidget import TakPGPlotWidget
from takagiabm.visualize.takagiwidgets.plotwidgets.pgbarwidget import  TakPGBarPlotWidget

def createDataShowWidget(counter, widgetClassName=""):
    '''

    '''
    if counter.chartType=='line':
        # if(widgetClassName.startswith('m')):
        #     t=TakMPLPlotWidget(name=counter.name,dataCounter=counter)
        #     counter.plotWidget=t
        #     return t
        # else:
        t = TakPGPlotWidget(name=counter.name, dataCounter=counter)
        counter.plotWidget = t
        return t
    elif counter.chartType=='bar':
        t=TakPGBarPlotWidget(name=counter.name,dataCounter=counter)
        counter.plotWidget=t
        return t

