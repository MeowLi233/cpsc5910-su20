from lab1.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD, ACTION_SUCK, ACTION_NOP

from lab1.vacuumagent import VacuumAgent
from lab1.agentstate import AgentState
from lab1.agentstate import NORTH, EAST, SOUTH, WEST
from lab1.agentstate import UNKNOWN, WALL, EDGE, DIRT, CLEAN
from lab1.agentstate import FORWARD, LEFT, RIGHT
          
"""
V7 agent -- placeholder for agent with "go home" feature
"""

VERSION = "V7"

DEFAULT_INITIAL_X = 1
DEFAULT_INITIAL_Y = 1
DEFAULT_INITIAL_DIRECTION = EAST

class V7Agent(VacuumAgent):

    def __init__(self, world_width, world_height, log, battery=300):
        super().__init__(VERSION, world_width, world_height, log, battery, self.execute)
        self.state = AgentState(world_width,\
                                world_height,\
                                DEFAULT_INITIAL_X,\
                                DEFAULT_INITIAL_Y,\
                                DEFAULT_INITIAL_DIRECTION)
        self.log = log

    def execute(self, percept):
        
        if self.battery_level <= 0:
            if self.battery_level != -999:
                self.log("Battery level is now 0. Halting!")
                self.log("Score: {}".format(self.score()))
                self.battery_level = -999
            self.state.update_action(ACTION_NOP)
            self.step_update(ACTION_NOP, percept)
            return ACTION_NOP
        
        action = ACTION_NOP
        self.step_update(action, percept)
        self.state.update_action(action)
        return action

         
