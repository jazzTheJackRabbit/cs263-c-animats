from AnimatView import Animat

class Predator(Animat):
    
    dictionaryOfPredators = dict()
    
    def __init__(self,width,height,color,grid):
        Animat.__init__(self, width, height, color, grid)
        Predator.dictionaryOfPredators[(self.gridX,self.gridY)] = self;
        
    def update(self):
        Animat.update(self)
        
    def move(self, directionX, directionY):
        oldXPosition = self.gridX
        oldYPosition = self.gridY
        Animat.move(self, directionX, directionY)
        Predator.dictionaryOfPredators.pop((oldXPosition,oldYPosition))
        while Predator.dictionaryOfPredators.has_key((self.gridX,self.gridY)):
            Animat.move(self, directionX, directionY)
        Predator.dictionaryOfPredators[(self.gridX,self.gridY)] = self;