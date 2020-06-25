from lab1.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD, ACTION_SUCK, ACTION_NOP

from lab1.vacuumagent import VacuumAgent
from lab1.agentstate import AgentState
from lab1.agentstate import NORTH, EAST, SOUTH, WEST
from lab1.agentstate import UNKNOWN, WALL, EDGE, DIRT, CLEAN
from lab1.agentstate import FORWARD, LEFT, RIGHT
          
"""
V6 agent -- placeholder for agent with "go home" feature
"""

VERSION = "V6"

DEFAULT_INITIAL_X = 1
DEFAULT_INITIAL_Y = 1
DEFAULT_INITIAL_DIRECTION = EAST

HOME_BONUS = 500

class V6Agent(VacuumAgent):

    def __init__(self, world_width, world_height, log, battery=300):
        super().__init__(VERSION, world_width, world_height, log, battery, self.execute)
        self.state = AgentState(world_width,\
                                world_height,\
                                DEFAULT_INITIAL_X,\
                                DEFAULT_INITIAL_Y,\
                                DEFAULT_INITIAL_DIRECTION)
        self.log = log

    def score(self):
        bonus = HOME_BONUS if (self.state.pos_x, self.state.pos_y) == (1,1) else 0
        return super().score() + bonus
    
    def execute(self, percept):
        
        if self.battery_level <= 0:
            if self.battery_level != -999:
                self.log("Battery level is now 0. Halting!")
                self.log("Score: {}".format(self.score()))
                self.battery_level = -999
            self.state.update_action(ACTION_NOP)
            self.step_update(ACTION_NOP, percept)
            return ACTION_NOP
        
        self.log(str(self.battery_level))
        action = ACTION_NOP
        self.step_update(action, percept)
        self.state.update_action(action)
        return action

         
