from AnimatView import Animat
from Predator import Predator

class Prey(Animat):
    
    dictionaryofPrey = dict()
    
    def __init__(self,width,height,color,grid):
        Animat.__init__(self, width, height, color, grid)
        Prey.dictionaryofPrey[(self._gridX,self._gridY)] = self
    
    def isNextMoveOnPredator(self,gridX,gridY):
        predatorPositionsInNeighborhood = self.getPredatorPositionsInNeighborhood(self._gridX, self._gridY)
        #could also check length of the predatorsPositionsInNeighborhood, if it's 0
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
        for j in range (-1,2):
            for i in range (-1,2):
                if((not (i==0 and j==0))):
                    neighborPosition = (self._gridX + i, self._gridY + j)
                    if(self.isWithinBounds(neighborPosition[0],neighborPosition[1])):
                        positionsOfNeighborGrids.append(neighborPosition)
        return positionsOfNeighborGrids
    
    def isMovementPossible(self,nextGridX,nextGridY):
        if(Animat.isMovementPossible(self, nextGridX, nextGridY)):
            return not self.isNextMoveOnPredator(nextGridX, nextGridY)
        
        
    