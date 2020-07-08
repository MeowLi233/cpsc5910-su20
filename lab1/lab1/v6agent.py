from lab1.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD, ACTION_SUCK, ACTION_NOP

from lab1.vacuumagent import VacuumAgent
from lab1.agentstate import AgentState
from lab1.agentstate import NORTH, EAST, SOUTH, WEST
from lab1.agentstate import UNKNOWN, WALL, EDGE, DIRT, CLEAN
from lab1.agentstate import FORWARD, LEFT, RIGHT
from random import randint
         
"""
V6 agent -- placeholder for agent with "go home" feature
"""

VERSION = "V6"

DEFAULT_INITIAL_X = 1
DEFAULT_INITIAL_Y = 1
DEFAULT_INITIAL_DIRECTION = EAST

HOME_BONUS = 500

BATTERY_LOW_THRESHOLD = 100

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
    
    def battery_low(self):
        return self.battery_level < BATTERY_LOW_THRESHOLD
    
    def execute(self, percept): 
        # World state gets percepts, updates state of some squares
        self.state.update(percept.attributes["dirt"], percept.attributes["bump"])
        
        if self.battery_level <= 0:
            if self.battery_level != -999:
                self.log("Battery level is now 0. Halting!")
                self.log("Score: {}".format(self.score()))
                self.battery_level = -999
            self.state.update_action(ACTION_NOP)
            self.step_update(ACTION_NOP, percept)
            return ACTION_NOP
        
        action = None
        if self.battery_low():
            action = self.go_home_mode(percept)
        else:
            action  = self.suck_mode(percept)
        self.step_update(action, percept)
        self.state.update_action(action)
        return action
    
                  # 1.  Always suck dirt
        # 2.  Always go forward if forward state is unknown
        # 3.  If state to the left is unknown, turn left
        # 4.  If state to the right is unknown, turn right
        # 5.  Otherwise choose randomly between forward, left, and right
    def suck_mode(self, percept): 
        action = None
        if self.state.state() == DIRT:
            action = ACTION_SUCK
        elif self.state.state_forward() == UNKNOWN:
            action = ACTION_FORWARD
        elif self.state.state_in_direction(LEFT) == UNKNOWN:
            action = ACTION_TURN_LEFT
        elif self.state.state_in_direction(RIGHT) == UNKNOWN:
            action = ACTION_TURN_RIGHT
        else:
            r = randint(1,3)
            if r == 1:
                action = ACTION_FORWARD
            elif r == 2:
                action = ACTION_TURN_LEFT
            else:
                action = ACTION_TURN_RIGHT
        return action

         
