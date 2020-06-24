from lab1.vacuumagent import VacuumAgent
from lab1.agentstate import AgentState
from lab1.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD, ACTION_SUCK, ACTION_NOP
from lab1.agentstate import NORTH, EAST, SOUTH, WEST
from lab1.agentstate import UNKNOWN, WALL, EDGE, DIRT, CLEAN
from lab1.agentstate import FORWARD, LEFT, RIGHT

"""
V4 agent -- placeholder for V3 agent that works well for unevenly distributed dirt
"""

VERSION = "V4"

DEFAULT_INITIAL_X = 1
DEFAULT_INITIAL_Y = 1
DEFAULT_INITIAL_DIRECTION = EAST

def vacant(state):
    return state == DIRT or state == CLEAN  
 
class V4Agent(VacuumAgent):
 
    def __init__(self, world_width, world_height, log, battery=300):
        super().__init__(VERSION, world_width, world_height, log, battery, self.execute)
        self.state = AgentState(world_width,\
                                world_height,\
                                DEFAULT_INITIAL_X,\
                                DEFAULT_INITIAL_Y,\
                                DEFAULT_INITIAL_DIRECTION)
        self.log = log
        self.sweep_actions = []

    def battery_low(self, percept):
        if self.battery_level <= 0:
            if self.battery_level != -999:
                self.log("Battery level is now 0. Halting!")
                self.log("Score: {}".format(self.score()))
                self.battery_level = -999
            return ACTION_NOP
        
    def execute(self, percept): 
        self.state.update(percept.attributes["dirt"], percept.attributes["bump"])
        action = self.battery_low(percept)
        if action == None:
            if len(self.sweep_actions) == 0:
                action = self.execute_normally(percept)
            else:
                action = self.execute_sweep(percept)
        self.step_update(action, percept)
        self.state.update_action(action)
        self.log(f"Action {action}")
        return action
    
    def execute_normally(self, percept):
        self.log(f"Executing normally, percept is {percept.attributes}")
        action = None
        if self.state.state() == DIRT:
            action = ACTION_SUCK
            self.sweep_actions = [ACTION_FORWARD,
                                  ACTION_TURN_LEFT,
                                  ACTION_FORWARD,
                                  ACTION_TURN_LEFT, 
                                  ACTION_FORWARD,
                                  ACTION_FORWARD, 
                                  ACTION_TURN_LEFT,
                                  ACTION_FORWARD,
                                  ACTION_FORWARD,
                                  ACTION_FORWARD]
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
        return action
    
    def execute_sweep(self, percept):
        action = None
        if self.state.state() == DIRT:
            action = ACTION_SUCK
        else:
            action = self.sweep_actions.pop(0)
        return action
        
'''
VERSION = "V4"

class V4Agent(VacuumAgent):
 
    def __init__(self, world_width, world_height, log, battery=300):
        super().__init__(VERSION, world_width, world_height, log, battery, self.execute)

    def execute(self, percept): 
        if self.battery_level <= 0:
            if self.battery_level != -999:
                self.log("Battery level is now 0. Halting!")
                self.log("Score: {}".format(self.score()))
                self.battery_level = -999
            self.step_update(ACTION_NOP, percept)
            return ACTION_NOP
        
        action = ACTION_SUCK
        # Compute battery level and score
        self.step_update(action, percept)
        return action
'''