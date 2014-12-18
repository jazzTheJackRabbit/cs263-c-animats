import Predator

from AnimatObject import Animat
from Food import Food
from Obstacle import Obstacle
import qlearn_mod_random as qlearn
from Actions import Actions
import numpy as np
import Game

class Prey(Animat):
        
    dictionaryOfPreys= dict()
    
    def __init__(self,width,height,color,grid):
        Animat.__init__(self, width, height, color, grid)
        self.ai = qlearn.QLearn(actions=range(Actions.directions),alpha=0.1, gamma=0.9, epsilon=0.1)
        self.eaten = 0
        self.group = None  
        self.freeAgentList = None
        Prey.dictionaryOfPreys[(self.gridX,self.gridY)] = self
        
        gameInstance = Game.Game.singletonInstance
        gameInstance.freeAgentList.append(self)
#         if(self.freeAgentList != None): 
        self.freeAgentList = gameInstance.freeAgentList
    
    ###Instance Variables####    
    
    @property
    def eaten(self):
        return self._eaten
    
    @eaten.setter
    def eaten(self,value):
        self._eaten = value
        
    @property
    def group(self):
        return self._group
    
    @group.setter
    def group(self,value):        
        self._group = value
    
    @property
    def freeAgentList(self):
        return self._freeAgentList
    
    @freeAgentList.setter
    def freeAgentList(self,value):
        self._freeAgentList = value
        
    ###Instance Methods####
        
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
        return
        #Override this for all subclasses
#         state = self.calculateState()
#         reward = -20
#         
#         #Check if the animat is on a food Intensity gradient                
#         if(self.rewardForProximityToFood()):
#             reward +=  -1*(1 - self.rewardForProximityToFood())
#             
#         if(self.hasPredatorInNeighborhood()):
#             reward += -40
#             
#         if (self.gridX,self.gridY) in self.previousPositionTuples:
#             reward += -20
#             
#         #Check if the animat has been eaten by any of the predators        
#         if(self.isBeingEatenByPredator()):
#             self.eaten += 1
#             reward = -200
#             if self.lastState is not None:
#                 self.ai.learn(self.lastState,self.lastAction,reward,state)
#                 
#             #Since the prey will be re-spawned, reset the last state
#             self.lastState = None
#             self.respawnAtRandomPosition()
#             return
#         
#         if(self.isEatingFood()):
#             #Remove the food being eaten
#             eatenFood = Food.dictionaryOfFoodObjects.pop((self.gridX,self.gridY))
#             eatenFood.gotEaten()
#             eatenFoodCell = self.grid.cellMatrix[eatenFood.gridX][eatenFood.gridY]
#             eatenFoodCell.foodIntensity = 0
#             eatenFood = None
#             self.fed += 1
#             reward += 100
#         
#         #Reward for being in between offspring and predator
#         reward += self.rewardForProtection()            
#             
#         if(self.lastState is not None):
#             self.ai.learn(self.lastState,self.lastAction,reward,state)
#             
#         state = self.calculateState()
#         action = self.ai.chooseAction(state)
#         self.lastState = state
#         self.lastAction = action
#         self.setPrevious2Positions()
#         self.performAction(action)
#         self.drawGameObjectAtCurrentPosition()    
    
    def hasPredatorInNeighborhood(self):
        predatorsInNeighborHood = self.getPredatorPositionsInNeighborhood()
        if(len(predatorsInNeighborHood) > 0):
            return True
        return False
    
    def isBeingEatenByPredator(self):
        isBeingEaten = self.isCellOnAnyPredator((self.gridX,self.gridY))
        if(isBeingEaten):
            if(self.group != None):
                if(self == self.group.groupLeader):
                    gameInstance = Game.Game.singletonInstance        
                    gameInstance.leaderPreyList.remove(self)
                self.group.removePreyFromGroup(self) #Auto selects new leader
            self.group = None 
            
            if(not self in self.freeAgentList):
                self.freeAgentList.append(self)
                
        return isBeingEaten
    
    def calculateState(self):
        def stateValueForNeighbor(neighborCellCoordinates):
            currentCellState = ()
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

    def getCellFoodIntensity(self,neighborCellCoordinates):
        cell = self.grid.cellMatrix[neighborCellCoordinates[0]][neighborCellCoordinates[1]]
        return cell.foodIntensity
        
    def hasNoObjectOnCell(self,gridCoordinatesOfCell):
        return (not (self.isCellOnAnyFood(gridCoordinatesOfCell))) and (not(self.isCellOnAnyObstacle(gridCoordinatesOfCell))) and (not(self.isCellOnAnyPredator(gridCoordinatesOfCell))) and not(self.getCellFoodIntensity(gridCoordinatesOfCell))
    
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
    
    def move(self, directionX, directionY):
        #Override for subclass
#         oldXPosition = self.gridX
#         oldYPosition = self.gridY
        Animat.move(self, directionX, directionY)
#         Prey.dictionaryOfPreys.pop((oldXPosition,oldYPosition))
#         Prey.dictionaryOfPreys[(self.gridX,self.gridY)] = self;
                
#         nextXPosition = self.gridX + directionX
#         nextYPosition = self.gridY + directionY
#         if(self.isMovementPossible(nextXPosition, nextYPosition)):
#             #If prey is in new position     
#             if(not Prey.dictionaryOfPrey.has_key((nextXPosition,nextYPosition))):
#                 #Another Prey is not on the next Position, so valid movement
#                 Animat.move(self, directionX, directionY)
#                 Prey.dictionaryOfPrey.pop((oldXPosition,oldYPosition))
#                 Prey.dictionaryOfPrey[(self.gridX,self.gridY)] = self;
        
    def respawnAtRandomPosition(self):
        #Override for subclass
        return
#         oldXPosition = self.gridX
#         oldYPosition = self.gridY
#         
#         randomX = random.randrange(0,self.grid.numberOfColumns)
#         randomY = random.randrange(0,self.grid.numberOfRows)
#         self.setXYPosition(randomX, randomY)
#                 
#         Prey.dictionaryOfPrey.pop((oldXPosition,oldYPosition))
#         while Prey.dictionaryOfPrey.has_key((self.gridX,self.gridY)):
#             randomX = random.randrange(0,self.grid.numberOfColumns)
#             randomY = random.randrange(0,self.grid.numberOfRows)
#             self.setXYPosition(randomX, randomY)
#         Prey.dictionaryOfPrey[(self.gridX,self.gridY)] = self        
        
    def rewardForProximityToFood(self):        
        cell = self.grid.cellMatrix[self.gridX][self.gridY]        
        return cell.foodIntensity
            
    def findAngleTo(self,x1,y1):
        pi = np.pi
        x0 = self.gridX
        y0 = self.gridY
        deltaX = x1 - x0
        deltaY = y1 - y0
        if(deltaX == 0):
            deltaX = 0.000000001
        theta = None
        
        slope = deltaY/deltaX
        
        if deltaX >= 0:
            #Q1 or Q4
            if deltaY >= 0:
                #Q1
                theta = np.arctan(slope)
            else:
                #Q4
                theta = 2*pi + np.arctan(slope)
        else:
            #Q2 or Q3
            if deltaY >= 0:
                #Q2
                theta = pi + np.arctan(slope)
            else:
                #Q3
                theta = 3*pi/2 - np.arctan(slope)
        
        return round(theta * 180 / pi)
    
    def isWithinRangeOfAnyLeader(self,leader):
        distanceToLeader = ((leader.gridX - self.gridX)**2+(leader.gridY - self.gridY)**2)**0.5
        if(distanceToLeader <= 2):
            return True
        else:
            return False
        
    def isCellOnAnyLeader(self,gridCoordinatesOfCell):
        gameInstance = Game.Game.singletonInstance
        leaderList = gameInstance.leaderPreyList
        for leader in leaderList:
            if(gridCoordinatesOfCell == (leader.gridX,leader.gridY)):
                return True
            return False
        
    def findLeaderInNeighborhood(self):
        gameInstance = Game.Game.singletonInstance
        preyLeaders = gameInstance.leaderPreyList
        
        if(self.group == None):
            for leader in preyLeaders:
                if(self.isWithinRangeOfAnyLeader(leader)):
                    return leader
        elif(self.group.groupLeader != None):
            return self.group.groupLeader
        
        return None
        
    def removeSelfFromGroup(self):
        group = self.group
        group.removePreyFromGroup(self)
                
                
    
        
   
        
    