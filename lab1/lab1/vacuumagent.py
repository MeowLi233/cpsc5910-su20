# -*- coding: utf-8 -*-

from lab1.liuvacuum import Agent
from lab1.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD, ACTION_SUCK, ACTION_NOP

class VacuumAgent(Agent):
    def __init__(self, version, world_width, world_height, log, battery, exec):
        super().__init__(exec)
        self.version = version
        self.world_width = world_width
        self.world_height = world_height
        self.log = log
        self.battery_level = battery
        self._score = 0
        self.action_power_consumption = {ACTION_TURN_LEFT: 1, 
                                         ACTION_TURN_RIGHT: 1, 
                                         ACTION_FORWARD: 2, 
                                         ACTION_SUCK:4, 
                                         ACTION_NOP:0}
        self.dirt_reward = 10
        self.last_action = ACTION_NOP
       
    def score(self):
        return self._score
    
    def step_update(self, action, percept):
        self.battery_level -= self.action_cost(action)
        self._score += self.action_reward(action, percept)
        self.last_action = action
        
    def action_cost(self, action):
        return self.action_power_consumption[action]
    
    def action_reward(self, action, percept):
        if (action == ACTION_SUCK and percept.attributes["dirt"]):
            return self.dirt_reward
        else:
            return 0
        
        
        
        
    