from random import randint
from lab1.vacuumagent import VacuumAgent
from lab1.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD, ACTION_SUCK, ACTION_NOP

"""
V1 Agent has no sensors -- it just chooses between possible 
actions randomly
"""
VERSION = "V1"

class V1Agent(VacuumAgent):
    
    def __init__(self, world_width, world_height, log, battery=300):
        super().__init__(VERSION, world_width, world_height, log, battery, self.execute)

    def execute(self, percept): 

        # Standard pattern for dealing with depleted battery -- repeated
        # in all agents
        
        if self.battery_level <= 0:
            if self.battery_level != -999:
                self.log("Battery level is now 0. Halting!")
                self.log("Score: {}".format(self.score()))
                self.battery_level = -999
            self.step_update(ACTION_NOP, percept)
            return ACTION_NOP
        
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
        self.step_update(action, percept)
        return action