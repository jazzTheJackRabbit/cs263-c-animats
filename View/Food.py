from GameObject import GameObject

class Food(GameObject):
    
    def __init__(self,width,height,color,grid):
        GameObject.__init__(self,width,height,color,grid)
        self._reward = 0
        