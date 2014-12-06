from GameObject import GameObject

class EnvironmentObject(GameObject):  
        
    def __init__(self,width,height,color,grid):
        GameObject.__init__(self,width,height,color,grid)
        #Already initialized at a random position by superclass
        self.reward = 0  
        
    @property
    def reward(self):
        return self._reward

    @reward.setter
    def reward(self,value):
        self._reward = value
                