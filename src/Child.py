import random
import Predator
import Parent
from Prey import Prey
from Parent import Parent

class Child(Prey):
    
    dictionaryOfChildren = dict()
    
    def __init__(self,width,height,color,grid):
        Prey.__init__(self,width,height,color,grid)
        Child.dictionaryOfChildren[(self.gridX,self.gridY)] = self
    
    def getparentPositionsInNeighborHood(self):
        parentKeys = Parent.dictionaryOfParents.keys()
        neighborGrids = self.getNeighborGridCoordinates()
        parentPositionsinNeighborhood= []
        for neighborGrid in neighborGrids:
            if(Parent.dictionaryOfParents.has_key(neighborGrid)):
                parentPositionsinNeighborhood.append(neighborGrid)
        return parentPositionsinNeighborhood
    
    