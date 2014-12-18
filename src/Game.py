import pygame
import random
from Grid import Grid
from Food import Food
from Obstacle import Obstacle
from Predator import Predator
from PreyAdult import PreyAdult
from PreyOffspring import PreyOffspring
from PreyGroup import PreyGroup
from Prey import Prey

class Colors:
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 200)
    LIGHT_BLUE = (200, 200, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 102, 0)
    

class Game:
    
    singletonInstance = None
    
    def __init__(self):
        #set the singleton for the game for global access
        if(Game.singletonInstance != None):
            return Game.singletonInstance
        
        Game.singletonInstance = self
        # initialize the game engine
        pygame.init()
        pygame.display.set_caption("CS263C - Animats Based Modeling Project") 
        self.clock = pygame.time.Clock()
        
        self.numberOfCellsInColumnsOrRows = 20
        self.margin = 5
        self.done = False
        
        self.widthOfCell = 20
        self.heightOfCell = 20
        self.sizeOfCell = 20
        
        self.maxGroupSize = 3 
        self.numberOfPreyAdults = 6
        self.numberOfPreyOffsprings = 0
        self.numberOfPredators = 3
        self.numberOfFoodObjects = 10
        self.numberOfObstacles = 0
        self.numberOfGroups = self.numberOfPreyAdults/self.maxGroupSize
        
        #New additions:
        self.leaderPreyList = [] #Array of leaders
        self.preyGroupsList = [] #Array of groups
        self.freeAgentList = [] #List of all prey not in groups
        
        self.sizeCalculation = self.widthOfCell * self.numberOfCellsInColumnsOrRows + (self.margin * (self.numberOfCellsInColumnsOrRows + 1))
        self.size = (self.sizeCalculation, self.sizeCalculation)
        
        self.screen = pygame.display.set_mode(self.size)
    
        # Environment Agents/Objects
        self.grid = Grid(self.numberOfCellsInColumnsOrRows,self.numberOfCellsInColumnsOrRows, self.sizeOfCell, self.screen, self.margin, pygame)
        # Always init obstacles before everything else, because you don't want food being init'd on top of obstacle 
        self.obstacles = [Obstacle(self.widthOfCell, self.heightOfCell, Colors.BLACK, self.grid) for i in range(0, self.numberOfObstacles)]
        self.predators = [Predator(self.widthOfCell, self.heightOfCell, Colors.RED, self.grid) for i in range(0, self.numberOfPredators)]
        self.preyAdults = [PreyAdult(self.widthOfCell, self.heightOfCell, Colors.GREEN, self.grid) for i in range(0, self.numberOfPreyAdults)]
        self.preyOffsprings = [PreyOffspring(self.widthOfCell, self.heightOfCell, Colors.CYAN, self.grid) for i in range(0, self.numberOfPreyOffsprings)]
        self.foodObjects = [Food(self.widthOfCell, self.heightOfCell, Colors.ORANGE, self.grid) for i in range(0, self.numberOfFoodObjects)]
        self.preyGroupsList = [PreyGroup() for i in range(0,self.numberOfGroups)]
    
        self.leaderInitialized = False
        
#         preyKeys = Prey.dictionaryOfPreys.keys()
#         for preyKey in preyKeys:
#             self.freeAgentList.append(Prey.dictionaryOfPreys[preyKey])
    
    @property
    def freeAgentList(self):
        return self._freeAgentList
    
    @freeAgentList.setter
    def freeAgentList(self,value):
        self._freeAgentList = value
    
    def resetGridReferences(self):
        for cellRow in self.grid.cellMatrix:
            for cell in cellRow:
                cell.prey = []
                cell.predators = []
                cell.obstacles = []
                cell.foods = []            
    
    def pickRandomLeaders(self,group):
        if(group.groupLeader in group.preyClan):
            return group.groupLeader
        
        childIsLeader = True
        i = 0
        while(childIsLeader):
            if(i < len(self.freeAgentList)):
                random_index = random.randrange(i,len(self.freeAgentList))
            else:
                random_index = len(self.freeAgentList) - 1
            if(isinstance(self.freeAgentList[random_index], PreyAdult)):
                childIsLeader = False
        temp = self.freeAgentList[random_index]
        self.freeAgentList[random_index] = self.freeAgentList[i]
        self.freeAgentList[i] = temp       
        leader = self.freeAgentList[i]            
        
        return leader
    
    def worldUpdate(self,showDisplay):       
        self.screen.fill(Colors.BLACK)    
        self.grid.drawGrid(Colors.WHITE)               
            
        self.resetGridReferences()
            
        foodKeys = Food.dictionaryOfFoodObjects.keys()
        if(len(foodKeys) < 1):
            foods = [Food(self.widthOfCell, self.heightOfCell, Colors.ORANGE, self.grid) for i in range(0, self.numberOfFoodObjects)]
        for foodObjectPosition in foodKeys:
            food = Food.dictionaryOfFoodObjects[foodObjectPosition]
            food.update()
            self.grid.cellMatrix[food.gridX][food.gridY].food = food
            food.createFoodGradientsInNeighbors(3)
            food.gradientsCreated = True
            
        obstacleKeys = Obstacle.dictionaryOfObstacles.keys()
        for obstaclePosition in obstacleKeys:
            obstacle = Obstacle.dictionaryOfObstacles[obstaclePosition]        
            obstacle.update()
            self.grid.cellMatrix[obstacle.gridX][obstacle.gridY].obstacle = obstacle
        
        predatorKeys = Predator.dictionaryOfPredators.keys()
        for predatorPosition in predatorKeys:
            predator = Predator.dictionaryOfPredators[predatorPosition]
            predator.update()
            self.grid.cellMatrix[predator.gridX][predator.gridY].predator = predator
        
        #Choose leaders
        if(len(self.leaderPreyList) < len(self.preyGroupsList)):
            leaderList = []
            for group in self.preyGroupsList:
                leaderList.append(self.pickRandomLeaders(group))
            #Add leaders to the group and make them leaders of respective groups
            for i in range(0,len(self.preyGroupsList)):     
                if isinstance(leaderList[i], PreyOffspring):
                    print leaderList[i]
                self.preyGroupsList[i].addPreyToGroup(leaderList[i]) #Just add prey to the group, they will automatically become leaders if they are the first ones in the group
#                 self.leaderPreyList[i].group = self.preyGroupsList[i]
#                 print self.leaderPreyList[i].group          
                     
        #Update leader positions
        if(len(self.leaderPreyList) > 0):
            for leader in self.leaderPreyList:
                self.grid.cellMatrix[leader.gridX][leader.gridY].preyAdult = leader
                leader.update()
        
        for group in self.preyGroupsList:
            for groupPrey in group.preyClan:
                if(groupPrey != group.groupLeader):
                    self.grid.cellMatrix[groupPrey.gridX][groupPrey.gridY].preyAdult = groupPrey
                    groupPrey.update() 
        
        if(len(self.freeAgentList) > 0):
            for singularPrey in self.freeAgentList:
                self.grid.cellMatrix[singularPrey.gridX][singularPrey.gridY].preyAdult = singularPrey
                singularPrey.update()
        #Update all other positions
        
#         preyAdultKeys = PreyAdult.dictionaryOfPreyAdults.keys()
#         for preyAdultPosition in preyAdultKeys:
#             singularAdultPrey = PreyAdult.dictionaryOfPreyAdults[preyAdultPosition]        
#             self.grid.cellMatrix[singularAdultPrey.gridX][singularAdultPrey.gridY].preyAdult = singularAdultPrey
#             singularAdultPrey.update()  
#             
#         offspringKeys = PreyOffspring.dictionaryOfOffsprings.keys()
#         for preyOffspringPosition in offspringKeys:
#             singular_preyoffspring = PreyOffspring.dictionaryOfOffsprings[preyOffspringPosition]        
#             self.grid.cellMatrix[singular_preyoffspring.gridX][singular_preyoffspring.gridY].offspring = singular_preyoffspring
#             singular_preyoffspring.update() 
                                  
        #Remove these animats from the freeAgentList array
        #TODO: when animats die, add them to the freeAgentList
        #Before every update
            #Update leaders positions first
            #Update animats position. 
                #Always check how far it is to any of the leaders.            
                    #If animat is located at a distance farther than 2d then
                        #if it was already part of a group make animat.group == None
                        #follow QTable
                    #If animat is located at a distance within 2d, then 
                        #Add to leaders group if not already in group
                        #follow leaders action  
                        #get good reward
                
        #Change from here
             
            
           
        #Change to here
        
        if(showDisplay):
            pygame.display.update()
            self.clock.tick(10)       
    
    def run(self):
        worldAge = 0
        endAge = worldAge + 50000
        while not self.done and worldAge < endAge:
            # --- Main event loop      
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.done = True            
            
            self.grid.shouldDrawScreen = True  
            self.worldUpdate(self.grid.shouldDrawScreen)
            
            if worldAge % 10000 == 0:
                preyAdultKeys = PreyAdult.dictionaryOfPreyAdults.keys()
                for preyAdultPosition in preyAdultKeys:
                    singular_prey = PreyAdult.dictionaryOfPreyAdults[preyAdultPosition]                                
                    print "{:d}, e: {:0.2f}, W: {:d}, L: {:d}, CP: {:d}"\
                        .format(worldAge, singular_prey.ai.epsilon, singular_prey.fed, singular_prey.eaten, singular_prey.offspringsProtected)
                    singular_prey.eaten = 0
                    singular_prey.fed = 0
                    singular_prey.offspringsProtected = 0
                    
            worldAge += 1
            
        while not self.done:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.done = True   
            
            self.grid.shouldDrawScreen = True    
            self.worldUpdate(self.grid.shouldDrawScreen)
            
        pygame.quit()
