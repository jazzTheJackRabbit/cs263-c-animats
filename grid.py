import pygame
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

#set the height and width of each cell
width = 20
height = 20

#starting location of bull
bull_x = 5
bull_y = 5

#set the margin between each cell
margin = 5 

#starting location of lion
lion_x = margin * 5 + width * 5 + margin
lion_y = margin * 5 + height * 5 + margin

#initialize the game engine
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (255, 255)
screen = pygame.display.set_mode(size)

#set title of screen
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
 
    # --- Game logic should go here
 
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)

    # --- Drawing code should go here
    # --- Drawing grid
    for column in range(0, 10):
        for rows in range(0,10):
            pygame.draw.rect(screen,WHITE,((margin+width)*column+margin,
                (margin+height)*rows+margin,width,height))


    # --- Drawing bull
    pygame.draw.rect(screen,GREEN, (bull_x, bull_y ,width,height));

    # --- Move bull
    bull_x += width+margin
 
    # --- Drawing lion
    pygame.draw.rect(screen,RED, (lion_x,lion_y,width,height));

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(10)
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()