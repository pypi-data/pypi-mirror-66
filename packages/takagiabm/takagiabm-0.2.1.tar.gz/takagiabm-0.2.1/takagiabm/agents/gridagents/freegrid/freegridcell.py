from takagiabm.agents.baseagent import BaseAgent
from takagiabm.toolbox.typeutils import getColorArr,getColorList
class Cell(BaseAgent):
    __slots__ = ('model', 'grid', 'properties')

    def __init__(self, pos, grid=None, model=None, color='#ffffff'):
        super().__init__(model=model, pos=pos)
        # self.pos=[pos[0],pos[1]]
        self.model = model
        self.grid = grid
        self.properties['color'] = color  # self.properties这个词典继承自Agent基类.

    def step(self):
        pass

    def getNeighbors(self, shape=''):
        return self.grid.getNeighbors(self.pos, shape)

    def getNeighborProperties(self, propertyName, shape=''):
        return self.grid.getNeighborProperties(self.pos, propertyName, shape)

    def __repr__(self):
        return 'cell at grid ,pos:' + str(self.pos)

    def setProperty(self, propertyName: str, property):
        if (type(propertyName) != type('')):
            raise Exception( \
                '警告:agent或者cell的属性只能以字符串命名.你输入的是%s' % (repr(property)))
        self.properties[propertyName] = property

    def setColor(self,color:str)->None:
        self.properties['color']=color
        self.grid.colorList[self.pos[1]][self.pos[0]]=getColorList(color)


    def onClicked(self):
        pass