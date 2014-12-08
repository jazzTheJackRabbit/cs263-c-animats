import pygame
from Grid import Grid
from Food import Food
from Obstacle import Obstacle
from Predator import Predator
from Prey import Prey

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 102, 0)

# initialize the game engine
pygame.init()
pygame.display.set_caption("My Game") 
clock = pygame.time.Clock()

numberOfCellsInColumnsOrRows = 15
margin = 5
done = False

widthOfCell = 20
heightOfCell = 20
sizeOfCell = 20

numberOfPreys = 4
numberOfPredators = 2
numberOfFoodObjects = 8
numberOfObstacles = 5

sizeCalculation = widthOfCell * numberOfCellsInColumnsOrRows + (margin * (numberOfCellsInColumnsOrRows + 1))
size = (sizeCalculation, sizeCalculation)

screen = pygame.display.set_mode(size)

# Environment Agents/Objects
grid = Grid(numberOfCellsInColumnsOrRows, numberOfCellsInColumnsOrRows, sizeOfCell, screen, margin, pygame)
# Always init obstacles before everything else, because you don't want food being init'd on top of obstacle 
[Obstacle(widthOfCell, heightOfCell, BLACK, grid) for i in range(0, numberOfObstacles)]
[Predator(widthOfCell, heightOfCell, RED, grid) for i in range(0, numberOfPredators)]
[Prey(widthOfCell, heightOfCell, BLUE, grid) for i in range(0, numberOfPreys)]
[Food(widthOfCell, heightOfCell, ORANGE, grid) for i in range(0, numberOfFoodObjects)]

# Reference to all animat agents in the environment
# environmentAgents = []
# [environmentAgents.append(predator) for predator in predators]
# [environmentAgents.append(prey) for singular_prey in prey]

def resetGridReferences():
    for cellRow in grid.cellMatrix:
        for cell in cellRow:
            cell.prey = []
            cell.predators = []
            cell.obstacles = []
            cell.foods = []

def worldUpdate(showDisplay):
                        
    screen.fill(BLACK)    
    grid.drawGrid(WHITE)               
        
    resetGridReferences()
        
    foodKeys = Food.dictionaryOfFoodObjects.keys()
    if(len(foodKeys) < 1):
        foods = [Food(widthOfCell, heightOfCell, ORANGE, grid) for i in range(0, numberOfFoodObjects)]
    for foodObjectPosition in foodKeys:
        food = Food.dictionaryOfFoodObjects[foodObjectPosition]
        food.update()
        grid.cellMatrix[food.gridX][food.gridY].food = food
        
    obstacleKeys = Obstacle.dictionaryOfObstacles.keys()
    for obstaclePosition in obstacleKeys:
        obstacle = Obstacle.dictionaryOfObstacles[obstaclePosition]        
        obstacle.update()
        grid.cellMatrix[obstacle.gridX][obstacle.gridY].obstacle = obstacle
    
    predatorKeys = Predator.dictionaryOfPredators.keys()
    for predatorPosition in predatorKeys:
        predator = Predator.dictionaryOfPredators[predatorPosition]
        predator.update()
        grid.cellMatrix[predator.gridX][predator.gridY].predator = predator
    
    preyKeys = Prey.dictionaryOfPrey.keys()
    for preyPosition in preyKeys:
        singular_prey = Prey.dictionaryOfPrey[preyPosition]        
        grid.cellMatrix[singular_prey.gridX][singular_prey.gridY].prey = singular_prey
        singular_prey.update()        
    
    if(showDisplay):
        pygame.display.update()
        clock.tick(10)       

worldAge = 0
endAge = worldAge + 150000
while not done and worldAge < endAge:
    # --- Main event loop      
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True            
    
    grid.shouldDrawScreen = False  
    worldUpdate(grid.shouldDrawScreen)
    
    if worldAge % 10000 == 0:
        preyKeys = Prey.dictionaryOfPrey.keys()
        for preyPosition in preyKeys:
            singular_prey = Prey.dictionaryOfPrey[preyPosition]                    
            mouse = singular_prey
            print "{:d}, e: {:0.2f}, W: {:d}, L: {:d}"\
                .format(worldAge, mouse.ai.epsilon, mouse.fed, mouse.eaten)
            mouse.eaten = 0
            mouse.fed = 0
            
    worldAge += 1
    
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True   
    
    grid.shouldDrawScreen = True    
    worldUpdate(grid.shouldDrawScreen)
    
pygame.quit()
