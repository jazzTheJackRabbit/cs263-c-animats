from Cell import Cell
import random 

class GameObject(Cell):     
    def __init__(self,width,height,color,grid):
        Cell.__init__(self,width,height,grid._margin)
        self._color = color
        self._grid = grid
        self.setup()
        
    def setup(self):
        self.initAtRandomPosition()
        
    def drawGameObjectAtCurrentPosition(self):
        self.drawCellOnGrid(self._gridX,self._gridY,self._color,self._grid._screen)
        
    def initAtRandomPosition(self):
        randomPositionCoordinates = self.generateRandomPosition()
        self.setXYPosition(randomPositionCoordinates[0],randomPositionCoordinates[1])
        
    def generateRandomPosition(self): 
        randomX = random.randrange(0,self._grid._numberOfColumns)
        randomY = random.randrange(0,self._grid._numberOfRows)
        return (randomX,randomY)
        
    def update(self):
        self.drawGameObjectAtCurrentPosition()