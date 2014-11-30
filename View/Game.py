import pygame
from Grid import Grid
from AnimatView import Animat
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

#initialize the game engine
pygame.init()
pygame.display.set_caption("My Game") 
clock = pygame.time.Clock()

size = (255, 255)
screen = pygame.display.set_mode(size)

margin = 5
done = False

grid = Grid(10,10,screen,pygame)
animat = Animat(20,20,RED,grid)
animat.setXYPosition(2,3)

animat2 = Animat(20,20,GREEN,grid)
animat2.setXYPosition(5,5)

flag = True
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
 
    screen.fill(BLACK)    
    grid.drawGrid(WHITE)            
    
    if flag:
        animat.moveAnimatOneStepInX()
        flag = not flag
    else:
#         animat.moveAnimatOneStepInY()
        flag = not flag
    
    animat.drawAnimatAtCurrentPosition()
    
    pygame.display.update()
    clock.tick(10)
    
pygame.quit()