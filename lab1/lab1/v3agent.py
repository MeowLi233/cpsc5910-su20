from random import randint
from lab1.vacuumagent import VacuumAgent
from lab1.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD, ACTION_SUCK, ACTION_NOP

"""
V3 Agent -- best possible agent that uses (just) its sensors
"""

VERSION = "V3"

class V3Agent(VacuumAgent):
  
    def __init__(self, world_width, world_height, log, battery=300):
        super().__init__(VERSION, world_width, world_height, log, battery, self.execute)

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

        action = ACTION_NOP
        self.step_update(action, percept)
        return action