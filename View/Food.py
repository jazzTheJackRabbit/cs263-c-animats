from GameObject import GameObject

class Food(GameObject):
    
    _reward = 0
    
    def __init__(self,width,height,color,grid):
        GameObject.__init__(self,width,height,color,grid)
        