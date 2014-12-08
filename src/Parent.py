import random
import Predator
import Child

from Prey import Prey
from Child import Child

class Parent(Prey):
    
    dictionaryOfParents = dict()
    
    def __init__(self,width,height,color,grid):
        Prey.__init__(self,width,height,color,grid)
        Parent.dictionaryOfParent[(self.gridX,self.gridY)] = self
    
    def getChildPositionsInNeighborHood(self):
        childKeys = Child.dictionaryOfChildren.keys()
        neighborGrids = self.getNeighborGridCoordinates()
        childrenPositionsinNeighborhood= []
        for neighborGrid in neighborGrids:
            if(Child.dictionaryOfChildren.has_key(neighborGrid)):
                childrenPositionsinNeighborhood.append(neighborGrid)
        return childrenPositionsinNeighborhood
    
        