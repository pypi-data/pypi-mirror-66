'''
这是一个交通载具与车站的仿真模型，对应的模型为
'''
from takagiabm.agents.baseagent import BaseAgent
class Vehicle(BaseAgent):
    def __init__(self, pos1d: float, speed1d, route):
        self.route = route
        self.heading = 90

        self.pos1d = pos1d
        self.speed1d = speed1d

        self.text = ''
        self.stationStoped = {0.3: False, 0.5: False, 0.8: False}
        self.stopped = False
        self.stopTime = 100


    def go(self):
        dt = 1  # 1秒为单位
        scale = 100  # 一单位等于100米
        speed = 20
        v = speed / scale * dt*self.speed1d# 这个公式是我胡乱写的，切勿仿真！
        self.pos1d += v
        # self.route.setPos(self.pos1d / 200)
        # print(self.pos1d)

    def arriveStation(self):
        for k in self.stationStoped.keys():
            if (abs(self.pos1d / 200 - k) <= 1 / 200) & (self.stationStoped[k] == False):
                return k
        return None

    def step(self):
        station = self.arriveStation()
        if (station != None):
            if (self.stopped):
                self.stopTime -= 1
            else:
                self.stopped = True
                self.stopTime = 100
                self.stationStoped[station] = True
        else:
            if (self.stopped):
                self.stopTime -= 1
                if (self.stopTime <= 0):
                    self.stopped = 0
            else:
                self.go()
