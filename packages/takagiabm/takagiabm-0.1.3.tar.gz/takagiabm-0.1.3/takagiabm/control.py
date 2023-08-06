import multiprocessing
import os


def defaultstep(obj):
    pass


def prepareAgent(agentClass=None, agentStepFunc=None, agentOnClicked=None):
    if (agentClass != None):
        agentClass.step = agentStepFunc
        if (agentOnClicked != None):
            agentClass.onClicked = agentOnClicked

    return agentClass


def prepareCell(cellClass=None, cellStepFunc=None, cellOnClicked=None):
    if (cellClass != None):
        cellClass.step = cellStepFunc
        if (cellOnClicked != None):
            cellClass.onClicked = cellOnClicked
    return cellClass


def prepareModel(modelClass=None, varList=[], dataCounterList=[], width=34, height=34,
                 agentActivationPolicy='casual', cellActivationPolicy='casual',bgcolor='#000000',
                 modelInitFunc=None, wrapPolicy=None):
    modelClass.varList = varList
    modelClass.dataCounters = dataCounterList
    modelClass.width = width
    modelClass.height = height

    modelClass.agentActivationPolicy = agentActivationPolicy
    modelClass.cellActivationPolicy = cellActivationPolicy
    modelClass.initAgents = modelInitFunc
    modelClass.wrapPolicy = wrapPolicy
    modelClass.bgColor=bgcolor
    return modelClass


def simStart(sourceFile, modelClass, noGUI=False, parallel=False, maxSteps=100):
    if (noGUI):
        if (parallel == True):
            simParallel(modelClass, cores=3)
        else:
            run(modelClass, maxSteps=maxSteps)


    else:
        from takagiabm.visualize.mainwindow import TakBaseWindow
        from pyqtgraph import mkQApp
        app = mkQApp()
        win = TakBaseWindow(sourceFile=sourceFile, modelClass=modelClass)
        win.show()
        app.exec_()


def simParallel(modelClass, cores=1, l=[1, 2, 3]):
    print('进程数', cores)
    pool = multiprocessing.Pool(processes=2)
    for i in range(len(l)):
        pool.apply_async(run, (modelClass, 10, l[i]))

    pool.close()
    pool.join()


def run(modelClass, maxSteps=10 ** 20):
    m = modelClass()
    while (1):
        step = m.currentStep
        print(os.getpid(), "进行到%d步" % step)
        m.step()
        if (step >= maxSteps):
            break

