from Cell import Cell

class Grid:
       
    def __init__(self,rowLength,columnLength,sizeOfCell,screen,margin,pygame):
        self.numberOfRows = rowLength
        self.numberOfColumns = columnLength
        self.screen = screen
        self.pygame = pygame
        self.margin = margin
        self.cellWidth = sizeOfCell
        self.cellHeight = sizeOfCell
        self.cellMatrix = []
        self.shouldDrawScreen = False
        self.createGrid()
       
    #---------------------------------------------------------------------
    #Instance Variables [Getters and Setters]
    #---------------------------------------------------------------------
     
    @property
    def numberOfRows(self):
        return self._numberOfRows
    
    @numberOfRows.setter
    def numberOfRows(self,value):
        self._numberOfRows = value
     
    @property
    def numberOfColumns(self):
        return self._numberOfColumns
    
    @numberOfColumns.setter
    def numberOfColumns(self,value):
        self._numberOfColumns = value
        
    @property
    def screen(self):
        return self._screen
    
    @screen.setter
    def screen(self,value):
        self._screen = value
    
    @property
    def pygame(self):
        return self._pygame
    
    @pygame.setter
    def pygame(self,value):
        self._pygame = value
        
    @property
    def cellWidth(self):
        return self._cellWidth
    
    @cellWidth.setter
    def cellWidth(self,value):
        self._cellWidth = value  

    @property
    def cellHeight(self):
        return self._cellHeight
    
    @cellHeight.setter
    def cellHeight(self,value):
        self._cellHeight = value 
     
    @property
    def cellMatrix(self):
        return self._cellMatrix
    
    @cellMatrix.setter
    def cellMatrix(self,value):
        self._cellMatrix = value    
        
     
    #---------------------------------------------------------------------
    #Class Methods
    #---------------------------------------------------------------------
    def createGrid(self):        
        for row in range(0, self.numberOfRows):
            cellRow = []
            for columns in range(0,self.numberOfColumns):
                cell = Cell(self.cellWidth,self.cellHeight,self.margin)
                cell.setGrid(self)                
                cellRow.append(cell)
            self.cellMatrix.append(cellRow)
    
    def drawGrid(self,cellColor):
        for rowIndex in range(0, self.numberOfRows):            
            for columnIndex in range(0,self.numberOfColumns):                
                self.cellMatrix[rowIndex][columnIndex].drawCellOnGrid(rowIndex,columnIndex,cellColor,self.screen)            
    