from GameObject import GameObject

class Obstacle(GameObject):
    
    #Static Variable - Class members
    dictionaryOfObstacles = dict()
        
    def __init__(self,width,height,color,grid):
        GameObject.__init__(self,width,height,color,grid)
        #Already initialized at a random position by superclass
        self._reward = 0  
        Obstacle.dictionaryOfObstacles[(self._gridX,self._gridY)] = True
             
        