from AnimatView import Animat

class Predator(Animat):
    
    dictionaryOfPredators = dict()
    
    def __init__(self,width,height,color,grid):
        Animat.__init__(self, width, height, color, grid)
        Predator.dictionaryOfPredators[(self._gridX,self._gridY)] = self;
        
    def update(self):
        Animat.update(self)
        
    def move(self, directionX, directionY):
        oldXPosition = self._gridX
        oldYPosition = self._gridY
        Animat.move(self, directionX, directionY)
        Predator.dictionaryOfPredators.pop((oldXPosition,oldYPosition))
        while Predator.dictionaryOfPredators.has_key((self._gridX,self._gridY)):
            Animat.move(self, directionX, directionY)
        Predator.dictionaryOfPredators[(self._gridX,self._gridY)] = self;