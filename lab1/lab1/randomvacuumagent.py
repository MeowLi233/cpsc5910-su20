from random import randint
from lab1.vacuumagent import VacuumAgent
from lab1.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD, ACTION_SUCK, ACTION_NOP

"""
Random Vacuum agent
"""
class RandomVacuumAgent(VacuumAgent):

    def __init__(self, world_width, world_height, log, battery=300):
        super().__init__(world_width, world_height, log, battery, self.execute)

    def execute(self, percept): 
        bump = percept.attributes["bump"]
        dirt = percept.attributes["dirt"]
        
        if self.battery_level <= 0:
            if self.battery_level != -999:
                self.log("Battery level is now 0. Halting!")
                self.log("Score: {}".format(self.score()))
                self.battery_level = -999
            self.step_update(ACTION_NOP, percept)
            return ACTION_NOP

        random_action = randint(1,8)
        action = None
        if dirt:
            action = ACTION_SUCK
        else:
            if random_action == 1:
                action = ACTION_TURN_LEFT
            elif random_action == 2:
                action = ACTION_TURN_RIGHT
            else:
                action = ACTION_FORWARD
         
        self.step_update(action, percept)
        return action