from random import randint
from venv.agents.vacuumagent import VacuumAgent
from venv.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD
from venv.liuvacuum import ACTION_SUCK, ACTION_NOP
from venv.liuvacuum import ACTION_MINE_GOLD, ACTION_SENSE_GOLD, ACTION_UNLOAD_GOLD

VERSION = "V1"

class V1Agent(VacuumAgent):
    
    def __init__(self, log, battery=300):
        super().__init__(VERSION, log, battery, self.execute)
        self.last_action = None

    def execute(self, percept): 
            
        action = None
        if self.battery_depleted():
            action = ACTION_NOP
        elif self.last_action != ACTION_SENSE_GOLD:
            action = ACTION_SENSE_GOLD
        else:
        #  Choose SUCK 50% of the time, FORWARD 30%, then 
        #  LEFT and RIGHT 10% each  
            r = randint(1,10)
            if r <= 5:
                action = ACTION_SUCK
            elif r <= 8:
                action = ACTION_FORWARD
            elif r <= 9:
                action = ACTION_TURN_LEFT
            else:
                action = ACTION_TURN_RIGHT
        
        # Need to notify superclass to update
        # score and battery usage
        self.last_action = action
        self.step_update(action, percept)
        self.log(f"Action {action}")
        return action
    
    def prep(self, recon):
        pass
        #self.log(f"I am PREPPED! {recon}")
