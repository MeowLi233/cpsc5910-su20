# -*- coding: utf-8 -*-

from lab1.liuvacuum import Agent
from lab1.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD, ACTION_SUCK, ACTION_NOP

class VacuumAgent(Agent):
    def __init__(self, version, world_width, world_height, log, battery, exec):
        # Agent superclass holds function call to have agent choose next action
        super().__init__(exec)
        # Version is documentation string only
        self.version = version
        # Dimension of the environment
        self.world_width = world_width
        self.world_height = world_height
        # Agent writes log messages by calling this function
        self.log = log
        # Remaining battery units
        self.battery_level = battery
        # Score bonuses and action power consumption
        self._score = 0
        self.action_battery_consumption = {ACTION_TURN_LEFT: 1, 
                                         ACTION_TURN_RIGHT: 1, 
                                         ACTION_FORWARD: 2, 
                                         ACTION_SUCK: 4, 
                                         ACTION_NOP: 0}
        self.dirt_reward = 10
        self.last_action = ACTION_NOP
         
    # Agent must call this on each call every time its execute
    # method is called -- update last action, score, and battery
    # consumption
    
    def step_update(self, action, percept):
        self.battery_level -= self.action_battery_consumption[action]
        self._score += self.action_reward(action, percept)
        self.last_action = action
        
    def action_reward(self, action, percept):
        if (action == ACTION_SUCK and percept.attributes["dirt"]):
            return self.dirt_reward
        else:
            return 0
        
    # Getter for agent score
    def score(self):
        return self._score
        
        
        
    