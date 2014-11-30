from Cell import Cell

class Grid:
    
    #__Class members
    _numberOfRows = 0
    _numberOfColumns = 0
    _margin = 5
    _cellWidth = 20
    _cellHeight = 20
    _cellMatrix = []
    _screen = None
    _pygame = None
    
    def __init__(self,rowLength,columnLength,screen,pygame):
        self._numberOfRows = rowLength
        self._numberOfColumns = columnLength
        self._screen = screen
        self._pygame = pygame
        self.createGrid()
        
    def createGrid(self):        
        for row in range(0, self._numberOfRows):
            cellRow = []
            for columns in range(0,self._numberOfColumns):
                cell = Cell(self._cellWidth,self._cellHeight,self._margin)
                cell.setGrid(self)                
                cellRow.append(cell)
            self._cellMatrix.append(cellRow)
    
    def drawGrid(self,cellColor):
        for rowIndex in range(0, self._numberOfRows):            
            for columnIndex in range(0,self._numberOfColumns):                
                self._cellMatrix[rowIndex][columnIndex].drawCellOnGrid(rowIndex,columnIndex,cellColor,self._screen)            
    