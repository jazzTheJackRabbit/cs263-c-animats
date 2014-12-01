import qlearn_mod_random as qlearn
import random
from AnimatView import Animat
from Predator import Predator
from Food import Food
from Obstacle import Obstacle
from Actions import Actions

class Prey(Animat):
    
    dictionaryofPrey = dict()
    
    def __init__(self,width,height,color,grid):
        Animat.__init__(self, width, height, color, grid)
        self.ai = None
        self.ai = qlearn.QLearn(actions=range(Actions.directions),alpha=0.1, gamma=0.9, epsilon=0.1)
        self.eaten = 0
        self.fed = 0
        self.lastState = None
        self.lastAction = None
        
        Prey.dictionaryofPrey[(self._gridX,self._gridY)] = self
    
    def isNextMoveOnPredator(self,gridX,gridY):
        predatorPositionsInNeighborhood = self.getPredatorPositionsInNeighborhood(self._gridX, self._gridY)
        #could also check length of the predatorsPositionsInNeighborhood, if it's 0
        if((gridX,gridY) in predatorPositionsInNeighborhood):
            return True
        else:
            return False
        
    def getPredatorPositionsInNeighborhood(self,gridX,gridY):
        neighborGrids = self.getNeighborGridCoordinates()
        predatorPositionsInNeighborhood = []
        for neighborGrid in neighborGrids:
            if(Predator.dictionaryOfPredators.has_key(neighborGrid)):
                predatorPositionsInNeighborhood.append(neighborGrid)
        return predatorPositionsInNeighborhood
    
    def getNeighborGridCoordinates(self):
        positionsOfNeighborGrids = []
        lookAroundDistance = 2        
        for i in range (-lookAroundDistance,lookAroundDistance + 1):
            for j in range (-lookAroundDistance,lookAroundDistance + 1):
                if((abs(i) + abs(j) <= lookAroundDistance) and (not (i==0 and j==0))):
                    neighborPosition = (self._gridX + i, self._gridY + j)
                    if(self.isWithinBounds(neighborPosition[0],neighborPosition[1])):
                        positionsOfNeighborGrids.append(neighborPosition)
                        
        return positionsOfNeighborGrids
    
    def isMovementPossible(self,nextGridX,nextGridY):
        return Animat.isMovementPossible(self, nextGridX, nextGridY)
#         if(Animat.isMovementPossible(self, nextGridX, nextGridY)):
#             return not self.isNextMoveOnPredator(nextGridX, nextGridY)
        
    def update(self):
        state = self.calculateState()
        reward = -1
        
        #Check if the animat has been eaten by any of the predators
        if(self.isBeingEatenByPredator()):
            self.eaten += 1
            reward = -100
            if self.lastState is not None:
                self.ai.learn(self.lastState,self.lastAction,reward,state)
            self.lastState = None
            self.respawnAtRandomPosition()
        
        if(self.isEatingFood()):
            #Remove the food being eaten
            Food.dictionaryOfFoodObjects.pop((self._gridX,self._gridY))
            self.fed += 1
            reward = 50            
        
        if(self.lastState is not None):
            self.ai.learn(self.lastState,self.lastAction,reward,state)
            
        state = self.calculateState()
        action = self.ai.chooseAction(state)
        self.lastState = state
        self.lastAction = action
        
        self.performAction(action)
        self.drawGameObjectAtCurrentPosition()
    
    def isBeingEatenByPredator(self):
        return self.isCellOnAnyPredator((self._gridX,self._gridY))
    
    def isCellOnAnyPredator(self,gridCoordinatesOfCell):
        predatorKeys = Predator.dictionaryOfPredators.keys() #Keys are tuples and Values are references to the actual predator object
        for predatorPosition in predatorKeys:
            if(gridCoordinatesOfCell == predatorPosition):
                return True
        return False
    
    def calculateState(self):
        def stateValueForNeighbor(neighborCellCoordinates):
            if self.isCellOnAnyPredator(neighborCellCoordinates):
                return 3
            elif self.isCellOnAnyFood(neighborCellCoordinates):
                return 2
            elif self.isCellOnAnyObstacle(neighborCellCoordinates):
                return 1
            else:
                return 0
        
        return tuple([stateValueForNeighbor(neighborCellCoordinates) for neighborCellCoordinates in self.getNeighborGridCoordinates()])
    
    def isEatingFood(self):
        return self.isCellOnAnyFood((self._gridX,self._gridY))
    
    def isCellOnAnyFood(self,gridCoordinatesForCell):
        if(Food.dictionaryOfFoodObjects.has_key(gridCoordinatesForCell)):            
            return True
        return False
    
    def isCellOnAnyObstacle(self,gridCoordinatesForCell):
        if(Obstacle.dictionaryOfObstacles.has_key(gridCoordinatesForCell)):            
            return True
        return False
    
    def move(self, directionX, directionY):
        oldXPosition = self._gridX
        oldYPosition = self._gridY
        Animat.move(self, directionX, directionY)
        Prey.dictionaryofPrey.pop((oldXPosition,oldYPosition))
        while Prey.dictionaryofPrey.has_key((self._gridX,self._gridY)):
            Animat.move(self, directionX, directionY)
        Prey.dictionaryofPrey[(self._gridX,self._gridY)] = self;
        
    def respawnAtRandomPosition(self):
        oldXPosition = self._gridX
        oldYPosition = self._gridY
        
        randomX = random.randrange(0,self._grid._numberOfColumns)
        randomY = random.randrange(0,self._grid._numberOfRows)
        self.setXYPosition(randomX, randomY)
                
        Prey.dictionaryofPrey.pop((oldXPosition,oldYPosition))
        while Prey.dictionaryofPrey.has_key((self._gridX,self._gridY)):
            randomX = random.randrange(0,self._grid._numberOfColumns)
            randomY = random.randrange(0,self._grid._numberOfRows)
            self.setXYPosition(randomX, randomY)
        Prey.dictionaryofPrey[(self._gridX,self._gridY)] = self        
        
   
        
    