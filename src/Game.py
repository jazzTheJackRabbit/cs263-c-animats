import pygame
from Grid import Grid
from Food import Food
from Obstacle import Obstacle
from Predator import Predator
from Prey import Prey

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = ( 0,   0,   255)
ORANGE   = (255,102,0)

#initialize the game engine
pygame.init()
pygame.display.set_caption("My Game") 
clock = pygame.time.Clock()

numberOfCellsInColumnsOrRows = 10
margin = 5
done = False

widthOfCell = 20
heightOfCell = 20
sizeOfCell = 20

numberOfPreys = 1
numberOfPredators = 1
numberOfFoodObjects = 10
numberOfObstacles = 25

sizeCalculation = widthOfCell * numberOfCellsInColumnsOrRows + (margin * (numberOfCellsInColumnsOrRows + 1))
size = (sizeCalculation, sizeCalculation)

screen = pygame.display.set_mode(size)

#Environment Agents/Objects
grid = Grid(numberOfCellsInColumnsOrRows,numberOfCellsInColumnsOrRows,sizeOfCell,screen,margin,pygame)
#Always init obstacles before everything else, because you don't want food being init'd on top of obstacle
# TODO: random agent init to not be on top of obstacle 
[Obstacle(widthOfCell,heightOfCell,BLACK,grid) for i in range(0,numberOfObstacles)]
[Predator(widthOfCell,heightOfCell,RED,grid) for i in range(0,numberOfPredators)]
[Prey(widthOfCell,heightOfCell,BLUE,grid) for i in range(0,numberOfPreys)]
[Food(widthOfCell,heightOfCell,ORANGE,grid) for i in range(0,numberOfFoodObjects)]

#Reference to all animat agents in the environment
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

while not done:
    # --- Main event loop
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True 
 
    screen.fill(BLACK)    
    grid.drawGrid(WHITE)               
        
    resetGridReferences()
        
    foodKeys = Food.dictionaryOfFoodObjects.keys()
    if(len(foodKeys) < 1):
        foods = [Food(widthOfCell,heightOfCell,ORANGE,grid) for i in range(0,numberOfFoodObjects)]
    for foodObjectPosition in foodKeys:
        food = Food.dictionaryOfFoodObjects[foodObjectPosition]
        food.update()
        grid.cellMatrix[food.gridX][food.gridY].foods.append(food)
        
    obstacleKeys = Obstacle.dictionaryOfObstacles.keys()
    for obstaclePosition in obstacleKeys:
        obstacle = Obstacle.dictionaryOfObstacles[obstaclePosition]
        obstacle.update()
        grid.cellMatrix[obstacle.gridX][obstacle.gridY].obstacles.append(obstacle)
    
    predatorKeys = Predator.dictionaryOfPredators.keys()
    for predatorPosition in predatorKeys:
        predator = Predator.dictionaryOfPredators[predatorPosition]
        predator.update()
        grid.cellMatrix[predator.gridX][predator.gridY].predators.append(predator)
    
    preyKeys = Prey.dictionaryofPrey.keys()
    for preyPosition in preyKeys:
        singular_prey = Prey.dictionaryofPrey[preyPosition]
        singular_prey.update()
        grid.cellMatrix[singular_prey.gridX][singular_prey.gridY].prey.append(singular_prey)
    
    pygame.display.update()
    clock.tick(10)

pygame.quit()