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

sizeCalculation = widthOfCell * numberOfCellsInColumnsOrRows + (margin * (numberOfCellsInColumnsOrRows + 1))
size = (sizeCalculation, sizeCalculation)
screen = pygame.display.set_mode(size)


grid = Grid(numberOfCellsInColumnsOrRows,numberOfCellsInColumnsOrRows,sizeOfCell,screen,margin,pygame)

predator = Predator(widthOfCell,heightOfCell,RED,grid)

prey = Prey(widthOfCell,heightOfCell,BLUE,grid)

foods = [Food(widthOfCell,heightOfCell,ORANGE,grid) for i in range(0,10)]

obstacles = [Obstacle(widthOfCell,heightOfCell,BLACK,grid) for i in range(0,25)]

flag = True
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
 
    screen.fill(BLACK)    
    grid.drawGrid(WHITE)            
    
    predator.moveRandomly()
    prey.moveRandomly()
        
    foodObjectKeys = Food.dictionaryOfFoodObjects.keys()
    [Food.dictionaryOfFoodObjects[foodObjectPosition].drawGameObjectAtCurrentPosition() for foodObjectPosition in foodObjectKeys]
        
    obstacleKeys = Obstacle.dictionaryOfObstacles.keys()
    [Obstacle.dictionaryOfObstacles[obstaclePosition].drawGameObjectAtCurrentPosition() for obstaclePosition in obstacleKeys]
    
    predator.drawGameObjectAtCurrentPosition()
    prey.drawGameObjectAtCurrentPosition()
    
    if(prey._gridX == predator._gridX and prey._gridY == predator._gridY):
        break
    
    pygame.display.update()
    clock.tick(10)
    
pygame.quit()