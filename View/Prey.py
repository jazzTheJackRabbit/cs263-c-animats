from AnimatView import Animat
from Predator import Predator
from networkx.classes.function import neighbors

class Prey(Animat):
    
    dictionaryofPrey = dict()
    
    def __init__(self,width,height,color,grid):
        Animat.__init__(self, width, height, color, grid)
        Prey.dictionaryofPrey[(self._gridX,self._gridY)] = self
    
    def isNextMoveOnPredator(self,gridX,gridY):
        predatorPositionsInNeighborhood = self.getPredatorPositionsInNeighborhood(self._gridX, self._gridY)
        if((gridX,gridY) in predatorPositionsInNeighborhood):
            return True
        else:
            return False
        

    def getPredatorPositionsInNeighborhood(self,gridX,gridY):
        neighborGrids = self.getNeighborGrids()
        predatorPositionsInNeighborhood = []
        for neighborGrid in neighborGrids:
            if(Predator.dictionaryOfPredators.has_key(neighborGrid)):
                predatorPositionsInNeighborhood.append(neighborGrid)
        return predatorPositionsInNeighborhood
    
    
    def getNeighborGrids(self):
        positionsOfNeighborGrids = []
        for i in range (-1,2):
            for j in range (-1,2):
                neighborPosition = (self._gridX + i, self._gridY + j)
                if(self.isWithinBounds(neighborPosition[0],neighborPosition[1])):
                    positionsOfNeighborGrids.append(neighborPosition)
        return positionsOfNeighborGrids
    
    def isMovementPossible(self,nextGridX,nextGridY):
        if(Animat.isMovementPossible(self, nextGridX, nextGridY)):
            return self.isNextMoveOnPredator(nextGridX, nextGridY)
        
        
    