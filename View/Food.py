from GameObject import GameObject

class Food(GameObject):
    
    dictionaryOfFoodObjects = dict()
    
    def __init__(self,width,height,color,grid):
        GameObject.__init__(self,width,height,color,grid)
        self._reward = 0
        Food.dictionaryOfFoodObjects[(self._gridX,self._gridY)] = self
        