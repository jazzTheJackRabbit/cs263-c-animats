from GameObject import GameObject
from Obstacle import Obstacle
from Food import Food
from Actions import Actions

import random

class Animat(GameObject):   
    
    def __init__(self,width,height,color,grid):
        GameObject.__init__(self,width,height,color,grid)        
    
    def performAction(self,action):
        if action == Actions.MOVE_NORTH:
            self.move(0,1)
        elif action == Actions.MOVE_NORTHEAST:
            self.move(1,1) 
        elif action == Actions.MOVE_EAST:
            self.move(1,0)
        elif action == Actions.MOVE_SOUTHEAST:
            self.move(1,-1)
        elif action == Actions.MOVE_SOUTH:
            self.move(0,-1)  
        elif action == Actions.MOVE_SOUTHWEST:
            self.move(-1,-1)
        elif action == Actions.MOVE_WEST:
            self.move(-1,0)
        elif action == Actions.MOVE_NORTHWEST:
            self.move(-1,1)          
        
    def move(self,directionX,directionY):
        if(self.isMovementPossible(self.gridX + directionX, self.gridY + directionY)):
            self.gridX += directionX
            self.gridY += directionY
#             self.removeFoodIfAnimatIsOnFood(self._gridX, self._gridY)
#             self.drawGameObjectAtCurrentPosition()
    
    def isWithinBounds(self,gridX,gridY):
        if(gridX < 0 or gridX > self.grid.numberOfColumns-1 or gridY < 0 or gridY > self.grid.numberOfRows - 1):
            return False
        return True
           
    def isOnObstacle(self,gridX,gridY):
        if(Obstacle.dictionaryOfObstacles.has_key((gridX,gridY))):
            return True
        return False
        
    def setXYPosition(self,grid_x,grid_y): 
        if(self.isWithinBounds(grid_x,grid_y)):
            self.gridX = grid_x
            self.gridY = grid_y
            self.x = (grid_x + 1)*self.margin + (grid_x)*self.width
            self.y = (grid_y + 1)*self.margin + (grid_y)*self.height
                
    def moveRandomly(self):
        random_movement = random.randrange(0,8)  
        self.performAction(random_movement)       
            
    def isMovementPossible(self,nextGridX,nextGridY):
        if(self.isWithinBounds(nextGridX, nextGridY) and not self.isOnObstacle(nextGridX, nextGridY)):
            return True
        return False
    
    def update(self):
        self.moveRandomly()
        self.drawGameObjectAtCurrentPosition()
        
        