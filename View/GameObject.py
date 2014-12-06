from Cell import Cell
import random 

class GameObject(Cell):     
    def __init__(self,width,height,color,grid):
        Cell.__init__(self,width,height,grid.margin)
        self.color = color
        self.grid = grid
        self.setup()
    
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self,value):
        self._color = value
        
    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self,value):
        self._grid = value
        
    def setup(self):
        self.initAtRandomPosition()
        
    def drawGameObjectAtCurrentPosition(self):
        self.drawCellOnGrid(self.gridX,self.gridY,self.color,self.grid.screen)
        
    def initAtRandomPosition(self):
        randomPositionCoordinates = self.generateRandomPosition()
        self.setXYPosition(randomPositionCoordinates[0],randomPositionCoordinates[1])
        
    def generateRandomPosition(self): 
        randomX = random.randrange(0,self.grid.numberOfColumns)
        randomY = random.randrange(0,self.grid.numberOfRows)
        return (randomX,randomY)
        
    def update(self):
        self.drawGameObjectAtCurrentPosition()