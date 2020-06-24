from lab1.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD, ACTION_SUCK, ACTION_NOP

from lab1.vacuumagent import VacuumAgent
from lab1.agentstate import AgentState
from lab1.agentstate import NORTH, EAST, SOUTH, WEST
from lab1.agentstate import UNKNOWN, WALL, EDGE, DIRT, CLEAN
from lab1.agentstate import FORWARD, LEFT, RIGHT
  
from random import randint
        
"""
V3 agent -- has memory that lets it remember its location
and where it has been, and the state of each square
"""

VERSION = "V3"

DEFAULT_INITIAL_X = 1
DEFAULT_INITIAL_Y = 1
DEFAULT_INITIAL_DIRECTION = EAST

class V3Agent(VacuumAgent):

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

        self.state.update(percept.attributes["dirt"], percept.attributes["bump"])
        
        # 1.  Always suck dirt
        # 2.  Always go forward if forward state is unknown
        # 3.  If state to the left is unknown, turn left
        # 4.  If state to the right is unknown, turn right
        # 5.  Otherwise choose randomly between forward, left, and right
        

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
        
        self.step_update(action, percept)
        self.state.update_action(action)
        return action

        '''  SMART VERSION      
        # 1.  Always suck dirt
        # 2.  Always go forward if forward state is unknown
        # 3.  If state to the left is unknown, turn left
        # 4.  If state to the right is unknown, turn right
        # 5.  If forward, left, or right is vacant, go there
        # 6.  Otherwise just turn left and hope for the best :-)
        
        def vacant(state):
            return state == DIRT or state == CLEAN
        
    
        action = None
        if self.state.state() == DIRT:
            action = ACTION_SUCK
        elif self.state.state_forward() == UNKNOWN:
            action = ACTION_FORWARD
        elif self.state.state_in_direction(LEFT) == UNKNOWN:
            action = ACTION_TURN_LEFT
        elif self.state.state_in_direction(RIGHT) == UNKNOWN:
            action = ACTION_TURN_RIGHT
        elif vacant(self.state.state_forward()):
            action = ACTION_FORWARD
        elif vacant(self.state.state_in_direction(LEFT)):
            action = ACTION_TURN_LEFT
        elif vacant(self.state.state_in_direction(RIGHT)):
            action = ACTION_TURN_RIGHT
        else: action = ACTION_TURN_LEFT         
        '''       

         
