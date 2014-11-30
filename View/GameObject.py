from Cell import Cell
import random 

class GameObject(Cell):
    _grid = None
    _color = None
     
    def __init__(self,width,height,color,grid):
        Cell.__init__(self,width,height,grid._margin)
        self._color = color
        self._grid = grid
        self.initAtRandomPosition()
        
    def drawGameObjectAtCurrentPosition(self):
        self.drawCellOnGrid(self._gridX,self._gridY,self._color,self._grid._screen)
        
    def initAtRandomPosition(self):
        randomX = random.randrange(0,self._grid._numberOfColumns)
        randomY = random.randrange(0,self._grid._numberOfRows)
        self.setXYPosition(randomX, randomY)