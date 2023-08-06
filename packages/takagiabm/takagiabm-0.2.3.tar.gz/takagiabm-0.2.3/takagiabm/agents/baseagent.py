import numpy as np

from takagiabm.toolbox.typeutils import getColorArr
class BaseAgent():

    def __init__(self,pos,model=None):
        self.pos=np.array([0,0],dtype=np.int)
        self.pos=self.initPos(pos)
        self.master=None
        self.removed=False
        self.model=model
        self.properties={'color':'#000000'}

    def step(self)->None:
        pass
    def setColor(self,color:str)->None:
        self.properties['color']=color
    def getColor(self)->str:
        return self.properties['color']
    def getColorArray(self,pos=None)->np.array:# pos或者wh的输入都是tuple
        s = self.properties['color']
        return getColorArr(value=s)
        
    def setProperty(self,propertyName:str,property):
        if(type(propertyName)!=type('')):
            raise Exception(\
                '警告:agent或者cell的属性只能以字符串命名.你输入的是%s'%(repr(property)))
        self.properties[propertyName]=property

    def setTraitLater(self,propertyName:str,property):
        self.setPropertyLater(propertyName,property)
    def setPropertyLater(self,propertyName:str,property):# 待到下次访问的时候再设置.

        self.model.agentUpdateList.append((self,propertyName,property))
    def setTrait(self,traitName,trait):
        self.setProperty(traitName,trait)
    def getProperty(self,propertyName:str):# ->返回一个任何类型.
        if propertyName in self.properties.keys():
            return self.properties[propertyName]
        else:
            return None
    def getTrait(self,traitName:str):# ->返回一个任何类型.
        return self.getProperty(traitName)
    def initPos(self,pos):
        return np.array([pos[0],pos[1]])

    def setPos(self,pos):
        self.pos[0]=pos[0]
        self.pos[1]=pos[1]
    def getPosOnGrid(self):# 返回整数类型的。
        return np.floor(self.pos).astype(np.int)

    def onClicked(self):
        '''当鼠标点击网格时触发此功能'''
        pass

    def onKeyPressed(self):
        '''当键盘按下时触发此功能'''
        pass

    def onKeyPressedInSelection(self):
        pass
    

    
        
def main():
    a=GridAgent((0,0))
    a.setSpeed(np.array([1,0]))
    a.turn('RIGHT')
    pass

if __name__ == "__main__":
    main()
