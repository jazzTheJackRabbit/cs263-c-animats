import pygame
import random

from Grid import Grid
from AnimatView import Animat
from Food import Food
from Obstacle import Obstacle

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

numberOfCellsInColumnsOrRows = 20

margin = 5
done = False

widthOfCell = 20
heightOfCell = 20

sizeCalculation = widthOfCell * numberOfCellsInColumnsOrRows + (margin * (numberOfCellsInColumnsOrRows + 1))
size = (sizeCalculation, sizeCalculation)
screen = pygame.display.set_mode(size)


grid = Grid(numberOfCellsInColumnsOrRows,numberOfCellsInColumnsOrRows,screen,pygame)
animat = Animat(widthOfCell,heightOfCell,RED,grid)

animat2 = Animat(widthOfCell,heightOfCell,BLUE,grid)

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
    
    animat.moveRandomly()
    animat2.moveRandomly()
        
    [food.drawGameObjectAtCurrentPosition() for food in foods]
        
    [obstacle.drawGameObjectAtCurrentPosition() for obstacle in obstacles]
    
    animat.drawGameObjectAtCurrentPosition()
    animat2.drawGameObjectAtCurrentPosition()
    
    pygame.display.update()
    clock.tick(10)
    
pygame.quit()