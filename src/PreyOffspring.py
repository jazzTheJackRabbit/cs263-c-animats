from Prey import Prey
from Food import Food
import PreyAdult
import random

class PreyOffspring(Prey):
    
    dictionaryOfOffsprings= dict()
    
    def __init__(self,width,height,color,grid):
        Prey.__init__(self, width, height, color, grid)
        PreyOffspring.dictionaryOfOffsprings[(self.gridX,self.gridY)] = self
        
    def getPreyAdultPositionsInNeighborhood(self):
        neighborGrids = self.getNeighborGridCoordinates()
        preyAdultPositionsInNeighborhood = []
        for neighborGrid in neighborGrids:
            if(PreyAdult.PreyAdult.dictionaryOfPreyAdults.has_key(neighborGrid)):
                preyAdultPositionsInNeighborhood.append(neighborGrid)
        return preyAdultPositionsInNeighborhood
    
    def update(self):
        state = self.calculateState()
        reward = -20
        
        #Check if the animat is on a food Intensity gradient                
        if(self.rewardForProximityToFood()):
            reward +=  -1*(1 - self.rewardForProximityToFood())
            
        if(self.hasPredatorInNeighborhood()):
            reward += -40
            
        if (self.gridX,self.gridY) in self.previousPositionTuples:
            reward += -20
            
        #Check if the animat has been eaten by any of the predators        
        if(self.isBeingEatenByPredator()):
            self.eaten += 1
            reward = -200
            if self.lastState is not None:
                self.ai.learn(self.lastState,self.lastAction,reward,state)
                
            #Since the prey will be re-spawned, reset the last state
            self.lastState = None
            self.respawnAtRandomPosition()
            return
        
        if(self.isEatingFood()):
            #Remove the food being eaten
            eatenFood = Food.dictionaryOfFoodObjects.pop((self.gridX,self.gridY))
            eatenFood.gotEaten()
            eatenFoodCell = self.grid.cellMatrix[eatenFood.gridX][eatenFood.gridY]
            eatenFoodCell.foodIntensity = 0
            eatenFood = None
            self.fed += 1
            reward += 100    
            
        reward += self.rewardForProtection()    
            
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
            currentCellState = ()
            if self.isCellOnAnyPrey(neighborCellCoordinates):
                currentCellState += (5,)
            if self.isCellOnAnyPredator(neighborCellCoordinates):
                currentCellState += (4,)
            if self.isCellOnAnyFood(neighborCellCoordinates):
                currentCellState += (3,)
            if self.isCellOnAnyObstacle(neighborCellCoordinates):
                currentCellState = (2,)                        
            if self.hasNoObjectOnCell(neighborCellCoordinates):
                currentCellState = (0,)
                
            if bool(self.getCellFoodIntensity(neighborCellCoordinates)):
                currentCellState += (self.getCellFoodIntensity(neighborCellCoordinates),)
                
            return currentCellState
            
        return tuple([stateValueForNeighbor(neighborCellCoordinates) for neighborCellCoordinates in self.getNeighborGridCoordinates()])
    
    def move(self, directionX, directionY):
        oldXPosition = self.gridX
        oldYPosition = self.gridY        
        nextXPosition = self.gridX + directionX
        nextYPosition = self.gridY + directionY
        if(self.isMovementPossible(nextXPosition, nextYPosition)):
            #If prey is in new position     
            if(not PreyOffspring.dictionaryOfOffsprings.has_key((nextXPosition,nextYPosition))):
                #Another PreyOffspring is not on the next Position, so valid movement
                Prey.move(self, directionX, directionY)
                PreyOffspring.dictionaryOfOffsprings.pop((oldXPosition,oldYPosition))
                PreyOffspring.dictionaryOfOffsprings[(self.gridX,self.gridY)] = self;
    
    def isCellOnAnyPrey(self,gridCoordinatesOfCell):
        preyKeys = PreyAdult.PreyAdult.dictionaryOfPreyAdults.keys() #Keys are tuples and Values are references to the actual predator object
        for preyAdultPosition in preyKeys:
            if(gridCoordinatesOfCell == preyAdultPosition):
                return True
            return False
    
    def respawnAtRandomPosition(self):
        oldXPosition = self.gridX
        oldYPosition = self.gridY
        
        randomX = random.randrange(0,self.grid.numberOfColumns)
        randomY = random.randrange(0,self.grid.numberOfRows)
        self.setXYPosition(randomX, randomY)
                
        PreyOffspring.dictionaryOfOffsprings.pop((oldXPosition,oldYPosition))
        while PreyOffspring.dictionaryOfOffsprings.has_key((self.gridX,self.gridY)):
            randomX = random.randrange(0,self.grid.numberOfColumns)
            randomY = random.randrange(0,self.grid.numberOfRows)
            self.setXYPosition(randomX, randomY)
        PreyOffspring.dictionaryOfOffsprings[(self.gridX,self.gridY)] = self
        
    def isBehindAdultAndPredator(self,predator,preyAdult):
        angleToPredator = self.findAngleTo(predator.gridX, predator.gridY)
        angleToPreyAdult = self.findAngleTo(preyAdult.gridX, preyAdult.gridY)
        
        if abs(angleToPredator - angleToPreyAdult) == 0:
            return True
        else:
            return False
        
    def rewardForProtection(self):
        predatorPositionsInNeighborhood = self.getPredatorPositionsInNeighborhood()
        preyAdultPositionsInNeighborhood = self.getPreyAdultPositionsInNeighborhood()
        reward = 0
        for predatorPosition in predatorPositionsInNeighborhood:
            predator = self.grid.cellMatrix[predatorPosition[0]][predatorPosition[1]]
            for preyAdultPosition in preyAdultPositionsInNeighborhood:
                preyAdult = self.grid.cellMatrix[preyAdultPosition[0]][preyAdultPosition[1]]
                if self.isBehindAdultAndPredator(predator, preyAdult):
                    reward = 150
                    break
                else:
                    reward = -100
        return reward