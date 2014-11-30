from AnimatView import Animat

class Predator(Animat):
    
    dictionaryOfPredators = dict()
    
    def __init__(self,width,height,color,grid):
        Animat.__init__(self, width, height, color, grid)
        Predator.dictionaryOfPredators[(self._gridX,self._gridY)] = self;
    