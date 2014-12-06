from Obstacle import Obstacle
from EnvironmentObject import EnvironmentObject

class Food(EnvironmentObject):
    
    dictionaryOfFoodObjects = dict()
    
    def __init__(self,width,height,color,grid):
        EnvironmentObject.__init__(self,width,height,color,grid)
        self.reward = 0
        Food.dictionaryOfFoodObjects[(self.gridX,self.gridY)] = self  
    
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