import time
import numpy as np


class DataCounter():

    def __init__(self, name='数量', propertyName='', targets=['agent', 'cell'],
                 chartType='line'):
        s = set(targets)
        for t in targets:
            s.add(t.lower())
        self.targets = s
        self.name = name
        self.initialLength = 50  # 这个变量是存储数据的长度，同时也是存储空间不足的时候扩展存储空间的单位。
        self.storageLength = self.initialLength
        self.propertyName = propertyName
        self.resultDic = {'_steps': np.zeros(self.initialLength)}
        self.dataLength = 0  # 代表已收集的数据的长度，而非总存储空间的大小。
        self.chartType = chartType
        self.plotWidget = None
        self.plotWidgetUpdateInterval = 10
        self.stepsToUpdatePlotWidget = self.plotWidgetUpdateInterval

    def extendStorage(self):
        for k in self.resultDic.keys():
            self.resultDic[k] = np.r_[self.resultDic[k], np.zeros(self.initialLength)]
        self.storageLength += self.initialLength

    def count(self, agentList: list, currentStep=0):

        self.dataLength += 1
        if (self.dataLength > self.initialLength * 0.9):
            self.extendStorage()
        if (self.propertyName == '') | (self.propertyName == None):
            propertyDic = {'': len(agentList)}  # 如果propertyName传入空字符串，那么就直接统计数量。
        else:

            propertyDic = self.collectProperty(agentList, self.propertyName)

        for k in propertyDic.keys():
            if (k not in self.resultDic.keys()):
                self.resultDic[k] = np.zeros(self.storageLength)  # 如果没有这个属性，就重新建一个矩阵。
            self.resultDic[k][self.dataLength - 1] = propertyDic[k]
        self.resultDic['_steps'][self.dataLength - 1] = currentStep

        if self.stepsToUpdatePlotWidget <= 0:
            if (self.plotWidget == None):
                return
            else:
                if(self.chartType=="line"):
                    self.plotWidget.plot(self.getCollectedDataDic(),figureTitle=self.name)
                elif(self.chartType=='bar'):
                    self.plotWidget.plot(self.getLastDataDic(),figureTitle=self.name)
            self.stepsToUpdatePlotWidget = self.plotWidgetUpdateInterval
        else:
            self.stepsToUpdatePlotWidget -= 1
        # print('updateData',self.resultDic)
    def getLastDataDic(self):
        '''
        返回已经收集的最后一组数据。长度为1,用于饼图和条形图。
        '''
        dic = {}
        for k in self.resultDic.keys():
            dic[k] = self.resultDic[k][self.dataLength-1:self.dataLength]
        return dic

    def getCollectedDataDic(self):
        '''
        返回已经收集的、不为空的变量字典。长度为dataLength
        '''
        dic = {}
        for k in self.resultDic.keys():
            dic[k] = self.resultDic[k][0:self.dataLength]
        return dic

    def collectAttr(self, agentList: list, attr=None) -> dict:
        propertyDic = {}

        for agent in agentList:
            # print(attr)
            a = getattr(agent, attr)
            if a in propertyDic.keys():
                propertyDic[a] += 1
            else:
                propertyDic[a] = 1

        return propertyDic

    def collectProperty(self, agentList: list, property: str) -> dict:
        t = time.time()
        propertyDic = {}

        for agent in agentList:
            a = agent.getProperty(property)
            if a in propertyDic.keys():
                propertyDic[a] += 1
            else:
                propertyDic[a] = 1

        return propertyDic
