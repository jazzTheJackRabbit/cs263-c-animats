from Cell import Cell

class Animat(Cell):   
    
    _grid = None
    _color = None
    
    def __init__(self,width,height,color,grid):
        Cell.__init__(self,width,height,grid._margin)
        self._color = color
        self._grid = grid
    
    def moveAnimatOneStepInX(self):
        self._gridX += 1
    
    def moveAnimatOneStepInY(self):
        self._gridY += 1 
        
    def drawAnimatAtCurrentPosition(self):
        self.drawCellOnGrid(self._gridX,self._gridY,self._color,self._grid._screen)
    