from Prey import Prey
import Game
from PreyOffspring import PreyOffspring
from PreyAdult import PreyAdult
class PreyGroup:
    
    listOfGroups = []
    
    def __init__(self):
        self.groupLeader = None
        self.preyClan = []
        self.leadersAction = None
        self.leadersLastFedScore = 0
        
    ###Instance Variables####
    
    @property
    def groupLeader(self):
        return self._groupLeader
    
    @groupLeader.setter
    def groupLeader(self,value):
        self._groupLeader = value
        
    @property
    def preyClan(self):
        return self._preyClan
    
    @preyClan.setter
    def preyClan(self,value):
        self._preyClan = value
        
    @property
    def leadersAction(self):
        return self._leadersAction
    
    @leadersAction.setter
    def leadersAction(self,value):
        self._leadersAction = value
        
    def addPreyToGroup(self,prey):        
        self.preyClan.append(prey)
        prey.group = self
        gameInstance = Game.Game.singletonInstance
        gameInstance.freeAgentList.remove(prey)
        if(len(self.preyClan) == 1):
            self.electNewLeader()         
        
    def removePreyFromGroup(self,prey):
        if(prey == self.groupLeader):
            self.groupLeader = None
            
        if(prey in self.preyClan):
            self.preyClan.remove(prey)
        else:
            self.preyClan.remove(prey)
        
        gameInstance = Game.Game.singletonInstance
        gameInstance.freeAgentList.append(prey)
        newLeaderPrey = None
        if(len(self.preyClan) == 0):
            #find a free agent to become leader of this group
            self.groupLeader = None
            childIsLeader = True
            i=0
           
            while(childIsLeader or i >= len(prey.freeAgentList)):                
                if(isinstance(newLeaderPrey, PreyOffspring)):                    
                    i += 1
                else:
                    newLeaderPrey = prey.freeAgentList[i]
                    childIsLeader = False
            
            for freeAgentPrey in prey.freeAgentList:
                if(newLeaderPrey != freeAgentPrey and freeAgentPrey.fed > newLeaderPrey.fed):
                    newLeaderPrey = freeAgentPrey
            
            if(newLeaderPrey != None):            
                self.addPreyToGroup(newLeaderPrey)
                    
        elif(prey == self.groupLeader and len(self.preyClan) > 0):
            self.electNewLeader()
            
        prey.group = None
    
    def electNewLeader(self):        
        if(len(self.preyClan) > 0):
            #Choose the animat with the highest 'fed' number
            leader = self.preyClan[0]
            leaderFedScore = self.preyClan[0].fed
            for prey in self.preyClan:
                if(prey.fed > leaderFedScore and isinstance(prey,PreyAdult)):
                    leader = prey
                    leaderFedScore = prey.fed
            
            if(isinstance(leader, PreyOffspring)):
                print leader
            self.groupLeader = leader
            
            gameInstance = Game.Game.singletonInstance
            
            gameInstance.leaderPreyList.append(leader)