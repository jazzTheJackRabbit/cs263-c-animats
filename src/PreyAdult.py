import random
import PreyOffspring
import numpy as np

from Prey import Prey
from Food import Food

class PreyAdult(Prey):
    
    dictionaryOfPreyAdults = dict()
    
    def __init__(self,width,height,color,grid):
        Prey.__init__(self, width, height, color, grid)
        self.offspringsProtected = 0
        PreyAdult.dictionaryOfPreyAdults[(self.gridX,self.gridY)] = self        

    @property
    def offspringsProtected(self):
        return self._offspringsProtected
    
    @offspringsProtected.setter
    def offspringsProtected(self,value):
        self._offspringsProtected = value
                        
    def getOffspringPositionsInNeighborhood(self):
        neighborGrids = self.getNeighborGridCoordinates()
        offspringPositionsInNeighborhood = []
        for neighborGrid in neighborGrids:
            if(PreyOffspring.PreyOffspring.dictionaryOfOffsprings.has_key(neighborGrid)):
                offspringPositionsInNeighborhood.append(neighborGrid)
        return offspringPositionsInNeighborhood
    
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
        
        #Reward for being in between offspring and predator
        if(self.rewardForProtection() > 0):
            reward += self.rewardForProtection()
            self.offspringsProtected += 1            
            
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
            if self.isCellOnAnyOffspring(neighborCellCoordinates):
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

    
    def isCellOnAnyOffspring(self,gridCoordinatesOfCell):
        offspringKeys = PreyOffspring.PreyOffspring.dictionaryOfOffsprings.keys() #Keys are tuples and Values are references to the actual predator object
        for offspringPosition in offspringKeys:
            if(gridCoordinatesOfCell == offspringPosition):
                return True
            return False
    
    def move(self, directionX, directionY):
        oldXPosition = self.gridX
        oldYPosition = self.gridY        
        nextXPosition = self.gridX + directionX
        nextYPosition = self.gridY + directionY
        if(self.isMovementPossible(nextXPosition, nextYPosition)):
            #If prey is in new position     
            if(not PreyAdult.dictionaryOfPreyAdults.has_key((nextXPosition,nextYPosition))):
                #Another PreyAdult is not on the next Position, so valid movement
                Prey.move(self, directionX, directionY)
                PreyAdult.dictionaryOfPreyAdults.pop((oldXPosition,oldYPosition))
                PreyAdult.dictionaryOfPreyAdults[(self.gridX,self.gridY)] = self;
        
    def respawnAtRandomPosition(self):
        oldXPosition = self.gridX
        oldYPosition = self.gridY
        
        randomX = random.randrange(0,self.grid.numberOfColumns)
        randomY = random.randrange(0,self.grid.numberOfRows)
        self.setXYPosition(randomX, randomY)
                
        PreyAdult.dictionaryOfPreyAdults.pop((oldXPosition,oldYPosition))
        while PreyAdult.dictionaryOfPreyAdults.has_key((self.gridX,self.gridY)):
            randomX = random.randrange(0,self.grid.numberOfColumns)
            randomY = random.randrange(0,self.grid.numberOfRows)
            self.setXYPosition(randomX, randomY)
        PreyAdult.dictionaryOfPreyAdults[(self.gridX,self.gridY)] = self        
    
    def isInBetweenPredatorAndOffspring(self,predator,offspring):
        angleToPredator = self.findAngleTo(predator.gridX, predator.gridY)
        angleToOffspring = self.findAngleTo(offspring.gridX, offspring.gridY)
        
        if abs(angleToPredator - angleToOffspring) == 180:
            return True
        else:
            return False
        
    def rewardForProtection(self):
        predatorPositionsInNeighborhood = self.getPredatorPositionsInNeighborhood()
        offspringPositionsInNeighborhood = self.getOffspringPositionsInNeighborhood()
        reward = 0
        for predatorPosition in predatorPositionsInNeighborhood:
            predator = self.grid.cellMatrix[predatorPosition[0]][predatorPosition[1]]
            for offspringPosition in offspringPositionsInNeighborhood:
                offspring = self.grid.cellMatrix[offspringPosition[0]][offspringPosition[1]]
                if self.isInBetweenPredatorAndOffspring(predator, offspring):
                    reward = 150
                    break
                else:
                    reward = -100
        return reward
        
   
        
    