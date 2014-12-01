import pygame
import random

from Grid import Grid
from AnimatView import Animat
from Food import Food
from Obstacle import Obstacle
from Predator import Predator
from Prey import Prey
from GameObject import GameObject

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
predators = [Predator(widthOfCell,heightOfCell,RED,grid) for i in range(0,numberOfPredators)]
preys = [Prey(widthOfCell,heightOfCell,BLUE,grid) for i in range(0,numberOfPreys)]
foods = [Food(widthOfCell,heightOfCell,ORANGE,grid) for i in range(0,numberOfFoodObjects)]
obstacles = [Obstacle(widthOfCell,heightOfCell,BLACK,grid) for i in range(0,numberOfObstacles)]

#Reference to all animat agents in the environment
environmentAgents = []
[environmentAgents.append(predator) for predator in predators]
[environmentAgents.append(preys) for prey in preys]

while not done:
    # --- Main event loop
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True 
 
    screen.fill(BLACK)    
    grid.drawGrid(WHITE)               
        
    foodObjectKeys = Food.dictionaryOfFoodObjects.keys()
    [Food.dictionaryOfFoodObjects[foodObjectPosition].update() for foodObjectPosition in foodObjectKeys]
        
    obstacleKeys = Obstacle.dictionaryOfObstacles.keys()
    [Obstacle.dictionaryOfObstacles[obstaclePosition].update() for obstaclePosition in obstacleKeys]
    
    predatorKeys = Predator.dictionaryOfPredators.keys()
    [Predator.dictionaryOfPredators[predatorPosition].update() for predatorPosition in predatorKeys]
    
    preyKeys = Prey.dictionaryofPrey.keys()
    [Prey.dictionaryofPrey[preyPosition].update() for preyPosition in preyKeys]
    
    pygame.display.update()
    clock.tick(10)

pygame.quit()