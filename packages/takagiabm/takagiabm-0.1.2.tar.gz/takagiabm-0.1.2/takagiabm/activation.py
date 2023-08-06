import random
import time
import numpy as np
from multiprocessing import Process,Queue
from takagiabm.agent import GridAgent
from multiprocessing.managers import BaseManager
import multiprocessing
class MyManager(BaseManager):
    pass
MyManager.register('GridAgent',GridAgent)
inQueue=Queue(50)
class Activator():
    def __init__(self,model):
        self.agentSet=model.agentSet
        
        #self.processor=ParallelProcessor()
        
    def casualActivation(self,agentList):
        '''
        随意地激活,不是随机的.意思是将所有元素简单的按照哈希表的顺序激活.
        '''
##        agentList=list(self.agentList)
        
        for agent in agentList:
            agent.step()

    def randomActivation(self,agentList:list,activatePortion=1)->None:#activatePortion是指激活的agent所占的比例.
        t0=time.time()
        if(activatePortion<0-1e-9)|(activatePortion>1+1e-9):
            raise Exception("Invalid activatePortion.激活比例须在[0,1]闭区间以内.")
##        agentList=list(self.agentSet)
        agentNum=len(agentList)
        agentNumToActivate=int(agentNum*activatePortion)#选择要激活的个体数目.相当于是不放回的抽样.
        
        
        agentIndexArray=np.arange(agentNumToActivate)

        np.random.shuffle(agentIndexArray)# 生成乱序数组

        for index in agentIndexArray:
            if(agentList[index].removed==False):
                agentList[index].step()



    def parallelActivation(self,agentList,activatePortion=1):
        global inQueue
        t0=time.time()
        if(activatePortion<0-1e-9)|(activatePortion>1+1e-9):
            raise Exception("Invalid activatePortion.激活比例须在[0,1]闭区间以内.")
        agentNum=len(agentList)
        agentNumToActivate=int(agentNum*activatePortion)#选择要激活的个体数目.相当于是不放回的抽样.
        
        
        agentIndexArray=np.arange(agentNumToActivate)
        t1=time.time()
        np.random.shuffle(agentIndexArray)# 生成乱序数组
        t2=time.time()
        #self.pool = multiprocessing.Pool(processes = 1)
        from pathos.pools import ProcessPool
        self.pool=ProcessPool(nodes=1)
        #print(agentList)
        try:
            print(id(agentList[0]))
        except:
            pass
        self.pool.map(process,agentList)
##        for index in agentIndexArray:
##            self.pool.apply_async(process,(agentList[index]))
##        self.pool.map(process,agentList)
##            inQueue.put(agentList[index])
           # print(self.processor.inQueue.qsize())
##        self.pool.close()
##        self.pool.join()
        t3=time.time()
        
        print('tttfggggg',time.time()-t0)
        pass
class ParallelProcessor():
    def __init__(self):
        # global inQueue
         self.processList=[]
         #self.
         for i in range(1):
            self.processList.append(Process(target=process, args=(lock)))
            self.processList[i].daemon=True
            self.processList[i].start()
        
        
        
def process(a):
    #print('sss')
    print('id',id(a))
    print(a.properties['color'])
    a.properties['color']='#aaaaaa'
    print(2,a.properties['color'])
    a.step()
    
##    print('hahahah')
##    with lock:
##    #print('qsize',self.inQueue.qsize())
##        if(inQueue.empty()):
##            time.sleep(0.01)
##        else:
##            agent=inQueue.get()
##            agent.step()
         

    
