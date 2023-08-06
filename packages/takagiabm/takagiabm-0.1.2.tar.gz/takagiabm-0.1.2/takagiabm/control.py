import multiprocessing
import os
def simStart(sourceFile,modelClass,varList=[],noGUI=False,parallel=False,maxSteps=100):
    #timer = pg.QtCore.QTimer()
    modelClass.varList=varList
    if(noGUI):
        if(parallel==True):
            simParallel(modelClass,cores=3)
        else:
            run(modelClass,maxSteps=maxSteps)
        

    else:
        from takagiabm.visualize.mainwindow import TakBaseWindow
        from pyqtgraph import mkQApp
        app = mkQApp()
        #modelClass.# 模型的源代码路径
        win=TakBaseWindow(sourceFile=sourceFile,modelClass=modelClass,varList=varList)
        win.show()
        app.exec_()

def simParallel(modelClass,cores=1,l=[1,2,3]):
    print('进程数',cores)
    pool=multiprocessing.Pool(processes=2)
    for i in range(len(l)):
        pool.apply_async(run,(modelClass,10,l[i]))    
    
    pool.close()
    pool.join()
##    run(modelClass,10)
        


def run(modelClass,maxSteps=10**20):
    m=modelClass()
    #f=open('/home/hzy/Desktop/%dpid.txt'%os.getpid(),'w')
    while(1):
        step=m.currentStep
        print(os.getpid(),"进行到%d步"%step)
        m.step()
        if(step>=maxSteps):
            break
    
#        f.write(str(m.dataCollector.collectProperty(m.grid.getAllCellsIter(),'color'))+'\n')
    #f.close()
