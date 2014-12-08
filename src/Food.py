from Obstacle import Obstacle
from EnvironmentObject import EnvironmentObject

class Food(EnvironmentObject):
    
    dictionaryOfFoodObjects = dict()
    
    def __init__(self,width,height,color,grid):
        EnvironmentObject.__init__(self,width,height,color,grid)
        self.reward = 0
        self.gradientsCreated = False
        Food.dictionaryOfFoodObjects[(self.gridX,self.gridY)] = self  

    @property
    def gradientsCreated(self):
        return self._gradientsCreated
    
    @gradientsCreated.setter
    def gradientsCreated(self,value):
        self._gradientsCreated = value
           
    def isPossibleToPlaceAtLocation(self,nextGridX,nextGridY):
        if(self.isWithinBounds(nextGridX, nextGridY) and not self.isOnObstacle(nextGridX, nextGridY)):
            return True
        return False
    
    def isOnObstacle(self,gridX,gridY):
        if(Obstacle.dictionaryOfObstacles.has_key((gridX,gridY))):
            return True
        return False
    
    def isWithinBounds(self,gridX,gridY):
        if(gridX < 0 or gridX > self.grid.numberOfColumns-1 or gridY < 0 or gridY > self.grid.numberOfRows - 1):
            return False
        return True
    
    def setup(self):
        randomPositionCoordinates = self.generateRandomPosition()
        while(not self.isPossibleToPlaceAtLocation(randomPositionCoordinates[0], randomPositionCoordinates[1])):
            randomPositionCoordinates = self.generateRandomPosition()
        self.setXYPosition(randomPositionCoordinates[0],randomPositionCoordinates[1])

    def getNeighborGridCoordinates(self):
        neighborPositionsInRound = []
        for cellDistance in range(1,4):
            currentRoundNeighbors = []
            start = True
            hopIncrement = 1
            hopCount = 0
            (x,y) = (0,0)
            columnActivated = True
            while (x,y) != (-cellDistance,-cellDistance):
                if start:
                    (x,y) = (-cellDistance,-cellDistance)
                    start = False
        
                if columnActivated:
                    y = y + hopIncrement
                    hopCount += hopIncrement
                else:
                    x -= hopIncrement
                    hopCount += hopIncrement
        
                if hopCount == -(cellDistance)*2 or hopCount == (cellDistance*2):
                    hopIncrement = -1 * hopIncrement
                    columnActivated = not columnActivated
        
                if hopCount == 0:
                    columnActivated = not columnActivated
        
                currentRoundNeighbors.append((x,y))
            neighborPositionsInRound.append(currentRoundNeighbors)
        return neighborPositionsInRound
    
    def createFoodGradientsInNeighbors(self):
        cellPositionsInNeighborhood = self.getNeighborGridCoordinates()
        for neighborRoundCells in range(0,3):
            for cellPosition in cellPositionsInNeighborhood[neighborRoundCells]:
                cell = self.grid.cellMatrix[cellPosition[0]][cellPosition[1]]
                print cell.gridX, cell.gridY