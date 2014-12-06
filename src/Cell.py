class Cell(object):
    #---------------------------------------------------------------------
    #Initialization
    #---------------------------------------------------------------------
    def __init__(self,width,height,margin):
        self.width = width
        self.height = height
        self.margin = margin
        self.x = 0
        self.y = 0
        self.gridX = 0
        self.gridY = 0
        self.grid = None
        
        self.prey = []
        self.predators = []
        self.foods = []
        self.obstacles = []
                
    #---------------------------------------------------------------------
    #Instance Variables [Getters and Setters]
    #---------------------------------------------------------------------
    
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self,value):
        self._width = value
            
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self,value):
        self._height = value
    
    @property
    def margin(self):
        return self._margin
    
    @margin.setter
    def margin(self,value):
        self._margin = value
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self,value):
        self._x = value
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self,value):
        self._y = value
    
    @property
    def gridX(self):
        return self._gridX
    
    @gridX.setter
    def gridX(self,value):
        self._gridX = value
    
    @property
    def gridY(self):
        return self._gridY
    
    @gridY.setter
    def gridY(self,value):
        self._gridY = value
        
    @property
    def grid(self):
        return self._grid
    
    @grid.setter
    def grid(self,value):
        self._grid = value
        
    @property
    def prey(self):
        return self._prey
    
    @prey.setter
    def prey(self,value):
        self._prey = value
        
    @property
    def predators(self):
        return self._predators
    
    @predators.setter
    def predators(self,value):
        self._predators = value
        
    @property
    def foods(self):
        return self._foods
    
    @foods.setter
    def foods(self,value):
        self._foods = value
    
    @property
    def obstacles(self):
        return self._obstacles
    
    @obstacles.setter
    def obstacles(self,value):
        self._obstacles = value
    
    #---------------------------------------------------------------------
    #Class Methods
    #---------------------------------------------------------------------
    
    def setGrid(self,grid):
        self.grid = grid
        
    def drawCell(self,color,screen):
        self.grid.pygame.draw.rect(screen,color,(self.x,self.y,self.width,self.height))
        
    def drawCellOnGrid(self,grid_x,grid_y,color,screen):
        self.setXYPosition(grid_x, grid_y)        
        self.drawCell(color,screen)
    
    def setXYPosition(self,grid_x,grid_y): 
        self._gridX = grid_x
        self._gridY = grid_y
        self._x = (grid_x + 1)*self._margin + (grid_x)*self._width
        self._y = (grid_y + 1)*self._margin + (grid_y)*self._height
            