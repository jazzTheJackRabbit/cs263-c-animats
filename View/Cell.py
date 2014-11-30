class Cell:
    #__init
    def __init__(self,width,height,margin):
        self._width = width
        self._height = height
        self._margin = margin
        self._x = 0
        self._y = 0
        self._gridX = 0
        self._gridY = 0
        
    def setGrid(self,grid):
        self._grid = grid
        
    def drawCell(self,color,screen):
        self._grid._pygame.draw.rect(screen,color,(self._x,self._y,self._width,self._height))
        
    def drawCellOnGrid(self,grid_x,grid_y,color,screen):
        self.setXYPosition(grid_x, grid_y)        
        self.drawCell(color,screen)
    
    def setXYPosition(self,grid_x,grid_y): 
        self._gridX = grid_x
        self._gridY = grid_y
        self._x = (grid_x + 1)*self._margin + (grid_x)*self._width
        self._y = (grid_y + 1)*self._margin + (grid_y)*self._height