import numpy as np

from takagiabm.toolbox.typeutils import getColorArr
from takagiabm.toolbox.looks import takTriangle
import takagiabm.toolbox.kinematics as kinematics
from takagiabm.agents.baseagent import BaseAgent


    
class GridAgent(BaseAgent):
    '''
    在Grid上运动的Agent
    '''

    def __init__(self,pos=np.array([0,0]),model=None,color='#ffffff'):

        super().__init__(model=model,pos=pos)
        # self.pos = pos
        self.grid=None
        self.stat=0
        self.properties['color']=color
        self.traits=self.properties
        self.markerDic={}
        self.speed=np.array([0,1],dtype=np.float32)
        self.orientation=np.array([0,1],dtype=np.float32)
        self.vertArray = takTriangle# 一个顶点列表。



    def setSpeed(self,speed:np.ndarray):# 设置速度
        if ((speed[0] == 0)&(speed[1]==0))|((self.speed[0]==0)&(self.speed[1]==0)):
            self.speed = speed
            return
        else:
            d=self.speed.dot(speed)/(np.linalg.norm(self.speed) * np.linalg.norm(speed))
            angle = np.arccos(d)
            self.turn(angle)# 这个的目的主要是把它的各个顶点也转过来。
            self.speed=speed

            self.orientation=self.speed.copy()# 设置其指向不变！
    def setShape(self,shape:np.ndarray):
        if shape.shape[1]!=2:
            raise Exception('注意，每个顶点输入应为一个二维坐标！你输入的是%s'%repr(shape))
        self.vertArray=shape
    def setVertArray(self,vertArray:np.ndarray):
        self.vertArray = vertArray.copy()# 复制对象。
    def getVertArray(self):
        return self.vertArray
    def getCellColor(self)->str:
        return self.grid.getCellColor(self.getPosOnGrid())
    def turn(self,dir):

        self.speed,self.vertArray=kinematics.turnWithVert(dir,self.speed,self.vertArray)# 避免有0的情况发生


    def setCellColor(self,color:str)->None:
        '''
        设置当前Agent所在的单元格的颜色.
        '''

        self.grid.setCellColor(self.getPosOnGrid(),color)
        pass
    def setMarker(self,status,marker)->None:
        self.markerDic[status]=marker
    def setMarkers(self,markerDic:dict)->None:
        self.markerDic=markerDic
    def getMarkerDic(self)->dict:
        return self.markerDic
    def getMarker(self,status):
        if(status not in self.markerDic.keys()):
            raise KeyError('状态%s在属性字典中不存在.'%status)
        return self.markerDic[status]

    def move(self,deltaPos=None)->None:
        '''
        将Agent移动一个相对位置deltaPos.比如等于[1,-1]的时候为向右平移1格,下平移1格.
        并且会将速度改写为np.ndarray([1,1]).
        当没有参数输入时,将使得Agent按照其speed移动.
        
        '''
        
        if(type(deltaPos)==np.ndarray):
            self.speed[0]=deltaPos[0]
            self.speed[1]=deltaPos[1]
            self.grid.moveAgent(self,self.speed)
        else:
            self.grid.moveAgent(self,self.speed)
        self.orientation=self.speed
            
    def moveTo(self,pos:np.ndarray)->None:
        '''
        将Agent移动到某个单元格,以tuple表示.
        '''
        self.speed=pos-self.pos
        #p=np.array([int(pos[0]),int(pos[1])])
        # print(self.getPosOnGrid())
        self.grid.moveAgentTo(self,pos)# 将位置作为整数发送出去。

    def getAgents(self)->list:
        '''
        返回此Agent所在的单元格中所有Agent的列表.
        '''
        if(self.grid==None):
            raise Exception('当前Agent对象不属于任何Grid网格对象！')
        return self.getAgentsByPos(self.getPosOnGrid())
    def getAgentsByPos(self,pos:np.ndarray)->BaseAgent:
        return self.grid.getAgentsByPos(pos)
    def setGrid(self,grid)->None:
        self.grid=grid
    def getGrid(self,grid):
        '''
        返回一个Grid对象
        '''
        return self.grid
    def step(self):
        self.stat+=1

    def __repr__(self):
        return "cor:%s,v:%s,color:%s"%(str(self.pos),str(self.speed),self.getColor())
    def die(self):
        self.model.removeAgent(self)
    def kill(self,agent):
        if agent in self.model.agentSet:
            self.model.removeAgent(agent)
        else:
            raise Exception('%s这个代理人不在当前模型中，可能未加入或已经移除。'%repr(agent))
    def setPos(self,pos):
        self.pos[0]=pos[0]
        self.pos[1]=pos[1]
    def getPosOnGrid(self):# 返回整数类型的。
        return np.floor(self.pos).astype(np.int)


class MatGridAgent(GridAgent):
    def __init__(self,pos,model=None,color='#ffffff'):
        super().__init__(pos,model,color)
        self.id=0

    def setPos(self,pos):
        if(self.model!=None):

            self.model.stoDic['pos'][self.id]=np.array((pos[0],pos[1]),np.float)
            self.pos=self.model.stoDic['pos'][self.id]
            return
        else:
            self.pos=pos

    def setProperty(self,propertyName:str,property):
        if(self.model!=None):
            if(propertyName in self.model.stoDic.keys()):
                self.model.stoDic[propertyName][self.id]=property
                self.properties[propertyName]=self.model.stoDic[propertyName][self.id]
                return

        self.properties[propertyName]=property
    def getProperty(self,propertyName:str):

        return self.properties[propertyName]

    def move(self,deltaPos=None) ->None:
        super().move(deltaPos)
        self.model.stoDic['pos'][self.id]=self.pos
        self.pos= self.model.stoDic['pos'][self.id]
    def moveTo(self,pos:np.ndarray) ->None:
        super().moveTo(pos)

        self.model.stoDic['pos'][self.id]=self.pos
        self.pos= self.model.stoDic['pos'][self.id]
    def setPos(self,pos):
        self.pos[0]=pos[0]
        self.pos[1]=pos[1]
    def getPosOnGrid(self):# 返回整数类型的。
        return np.floor(self.pos).astype(np.int)

    
        
def main():
    a=GridAgent((0,0))
    a.setSpeed(np.array([1,0]))
    a.turn('RIGHT')
    pass

if __name__ == "__main__":
    main()
