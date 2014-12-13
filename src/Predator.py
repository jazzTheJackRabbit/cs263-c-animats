import Prey
import random
import qlearn_mod_random as qlearn
from AnimatObject import Animat
from Food import Food
from Obstacle import Obstacle
from Actions import Actions

class Predator(Animat):
    
    dictionaryOfPredators = dict()
    
    def __init__(self,width,height,color,grid):
        Animat.__init__(self, width, height, color, grid)
        self.ai = qlearn.QLearn(actions=range(Actions.directions),alpha=0.1, gamma=0.9, epsilon=0.1)
        Predator.dictionaryOfPredators[(self.gridX,self.gridY)] = self;
                        
    def getNeighborGridCoordinates(self):
        positionsOfNeighborGrids = []
        lookAroundDistance = 2        
        for i in range (-lookAroundDistance,lookAroundDistance + 1):
            for j in range (-lookAroundDistance,lookAroundDistance + 1):
                if((abs(i) + abs(j) <= lookAroundDistance) and (not (i==0 and j==0))):
                    neighborPosition = (self.gridX + i, self.gridY + j)
                    if(self.isWithinBounds(neighborPosition[0],neighborPosition[1])):
                        positionsOfNeighborGrids.append(neighborPosition)
        return positionsOfNeighborGrids
    
    def getPreyPositionsInNeighborhood(self):
        neighborGrids = self.getNeighborGridCoordinates()
        preyPositionsInNeighborhood = []
        for neighborGrid in neighborGrids:
            if(Prey.Prey.dictionaryOfPrey.has_key(neighborGrid)):
                preyPositionsInNeighborhood.append(neighborGrid)
        return preyPositionsInNeighborhood    
        
    def update(self):
        state = self.calculateState()
        reward = -1
        
        #Check if the animat has been eaten by any of the predators
        if (self.gridX,self.gridY) in self.previousPositionTuples:
            reward += -20
        
        elif(self.hasPreyInNeighborhood()):
            reward = 20
                             
        if(self.isEatingPrey()):
            #Prey re-spawns itself randomly, if it gets eaten
            self.fed += 1
            reward = 50            
                
        if(self.lastState is not None):
            self.ai.learn(self.lastState,self.lastAction,reward,state)
            
        state = self.calculateState()
        action = self.ai.chooseAction(state)
        self.lastState = state
        self.lastAction = action            
        self.setPrevious2Positions()
        self.performAction(action)
        self.drawGameObjectAtCurrentPosition()
    
    def calculateState(self):
        def stateValueForNeighbor(neighborCellCoordinates):
            if self.isCellOnAnyPrey(neighborCellCoordinates):
                return 3
            elif self.isCellOnAnyFood(neighborCellCoordinates):
                return 2
            elif self.isCellOnAnyObstacle(neighborCellCoordinates):
                return 1
            else:
                return 0
        
        return tuple([stateValueForNeighbor(neighborCellCoordinates) for neighborCellCoordinates in self.getNeighborGridCoordinates()])    
    
    def hasPreyInNeighborhood(self):
        preyInNeighborHood = self.getPreyPositionsInNeighborhood()
        if(len(preyInNeighborHood) > 0):
            return True
        return False
    
    def isEatingPrey(self):
        return self.isCellOnAnyPrey((self.gridX,self.gridY))
        
    def isCellOnAnyPrey(self,gridCoordinatesOfCell):
        preyKeys = Prey.Prey.dictionaryOfPrey.keys() #Keys are tuples and Values are references to the actual prey object
        for preyPosition in preyKeys:
            if(gridCoordinatesOfCell == preyPosition):
                return True
        return False
    
    def isCellOnAnyFood(self,gridCoordinatesForCell):
        if(Food.dictionaryOfFoodObjects.has_key(gridCoordinatesForCell)):            
            return True
        return False
    
    def isCellOnAnyObstacle(self,gridCoordinatesForCell):
        if(Obstacle.dictionaryOfObstacles.has_key(gridCoordinatesForCell)):            
            return True
        return False
    
    #TODO: Requires massive change for multiple Predators
    def move(self, directionX, directionY):
        oldXPosition = self.gridX
        oldYPosition = self.gridY        
        nextXPosition = self.gridX + directionX
        nextYPosition = self.gridY + directionY
        if(self.isMovementPossible(nextXPosition, nextYPosition)):
            #If prey is in new position     
            if(not Predator.dictionaryOfPredators.has_key((nextXPosition,nextYPosition))):
                #Another Prey is not on the next Position, so valid movement
                Animat.move(self, directionX, directionY)
                Predator.dictionaryOfPredators.pop((oldXPosition,oldYPosition))
                Predator.dictionaryOfPredators[(self.gridX,self.gridY)] = self;    