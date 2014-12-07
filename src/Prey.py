import random
import Predator

from AnimatObject import Animat
from Food import Food
from Obstacle import Obstacle
import qlearn_mod_random as qlearn
from Actions import Actions

class Prey(Animat):
    
    dictionaryOfPrey = dict()
    
    def __init__(self,width,height,color,grid):
        Animat.__init__(self, width, height, color, grid)
        self.ai = qlearn.QLearn(actions=range(Actions.directions),alpha=0.1, gamma=0.9, epsilon=0.1)
        self.eaten = 0
        Prey.dictionaryOfPrey[(self.gridX,self.gridY)] = self
            
    def getPredatorPositionsInNeighborhood(self):
        neighborGrids = self.getNeighborGridCoordinates()
        predatorPositionsInNeighborhood = []
        for neighborGrid in neighborGrids:
            if(Predator.Predator.dictionaryOfPredators.has_key(neighborGrid)):
                predatorPositionsInNeighborhood.append(neighborGrid)
        return predatorPositionsInNeighborhood
    
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
            
    def update(self):
        state = self.calculateState()
        reward = -1
        
        #Check if the animat has been eaten by any of the predators
        if(self.isBeingEatenByPredator()):
            self.eaten += 1
            reward = -100
            if self.lastState is not None:
                self.ai.learn(self.lastState,self.lastAction,reward,state)
                
            #Since the prey will be re-spawned, reset the last state
            self.lastState = None
            self.respawnAtRandomPosition()
            return
        
        if(self.hasPredatorInNeighborhood()):
            reward = -20
        
        if(self.isEatingFood()):
            #Remove the food being eaten
            Food.dictionaryOfFoodObjects.pop((self.gridX,self.gridY))
            self.fed += 1
            reward = 200            
        
        if(self.lastState is not None):
            self.ai.learn(self.lastState,self.lastAction,reward,state)
            
        state = self.calculateState()
        action = self.ai.chooseAction(state)
        self.lastState = state
        self.lastAction = action
        
        self.performAction(action)
        self.drawGameObjectAtCurrentPosition()    
    
    def hasPredatorInNeighborhood(self):
        predatorsInNeighborHood = self.getPredatorPositionsInNeighborhood()
        if(len(predatorsInNeighborHood) > 0):
            return True
        return False
    
    def isBeingEatenByPredator(self):
        return self.isCellOnAnyPredator((self.gridX,self.gridY))
    
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
        return self.isCellOnAnyFood((self.gridX,self.gridY))
    
    def isCellOnAnyPredator(self,gridCoordinatesOfCell):
        predatorKeys = Predator.Predator.dictionaryOfPredators.keys() #Keys are tuples and Values are references to the actual predator object
        for predatorPosition in predatorKeys:
            if(gridCoordinatesOfCell == predatorPosition):
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
    
    #TODO: Requires massive change for multiple Prey
    def move(self, directionX, directionY):
        oldXPosition = self.gridX
        oldYPosition = self.gridY
        Animat.move(self, directionX, directionY)
        Prey.dictionaryOfPrey.pop((oldXPosition,oldYPosition))
        while Prey.dictionaryOfPrey.has_key((self.gridX,self.gridY)):
            Animat.move(self, directionX, directionY)
        Prey.dictionaryOfPrey[(self.gridX,self.gridY)] = self;
        
    def respawnAtRandomPosition(self):
        oldXPosition = self.gridX
        oldYPosition = self.gridY
        
        randomX = random.randrange(0,self.grid.numberOfColumns)
        randomY = random.randrange(0,self.grid.numberOfRows)
        self.setXYPosition(randomX, randomY)
                
        Prey.dictionaryOfPrey.pop((oldXPosition,oldYPosition))
        while Prey.dictionaryOfPrey.has_key((self.gridX,self.gridY)):
            randomX = random.randrange(0,self.grid.numberOfColumns)
            randomY = random.randrange(0,self.grid.numberOfRows)
            self.setXYPosition(randomX, randomY)
        Prey.dictionaryOfPrey[(self.gridX,self.gridY)] = self        
        
   
        
    