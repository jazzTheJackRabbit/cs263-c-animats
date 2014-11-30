from Cell import Cell

class Grid:
       
    def __init__(self,rowLength,columnLength,sizeOfCell,screen,margin,pygame):
        self._numberOfRows = rowLength
        self._numberOfColumns = columnLength
        self._screen = screen
        self._pygame = pygame
        self._margin = margin
        self._cellWidth = sizeOfCell
        self._cellHeight = sizeOfCell
        self._cellMatrix = []
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
    