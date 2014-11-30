from Cell import Cell

class Animat(Cell):   
    
    _grid = None
    _color = None
    
    def __init__(self,width,height,color,grid):
        Cell.__init__(self,width,height,grid._margin)
        self._color = color
        self._grid = grid
    
    def moveAnimatOneStepInX(self):
        if(self.isWithinBounds(self._gridX+1, self._gridY)):
            self._gridX += 1
    
    def moveAnimatOneStepInY(self):
        if(self.isWithinBounds(self._gridX, self._gridY+1)):
            self._gridY += 1 
        
    def drawAnimatAtCurrentPosition(self):
        self.drawCellOnGrid(self._gridX,self._gridY,self._color,self._grid._screen)
    
    def isWithinBounds(self,gridX,gridY):
        if(gridX < 0 or gridX > self._grid._numberOfColumns-1 or gridY < 0 or gridY > self._grid._numberOfRows):
            return False
        return True
           
    
    def setXYPosition(self,grid_x,grid_y): 
        if(self.isWithinBounds(grid_x,grid_y)):
            self._gridX = grid_x
            self._gridY = grid_y
            self._x = (grid_x + 1)*self._margin + (grid_x)*self._width
            self._y = (grid_y + 1)*self._margin + (grid_y)*self._height
                