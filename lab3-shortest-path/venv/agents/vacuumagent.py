# -*- coding: utf-8 -*-

from agentdefs import Agent
from venv.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD
from venv.liuvacuum import ACTION_SUCK, ACTION_NOP
from venv.liuvacuum import ACTION_SENSE_GOLD, ACTION_MINE_GOLD, ACTION_UNLOAD_GOLD

DIRT_REWARD = 10
GOLD_REWARD = 100

BATTERY_CONSUMPTION = {ACTION_TURN_LEFT: 1,
                       ACTION_TURN_RIGHT: 1, 
                       ACTION_FORWARD: 2,
                       ACTION_SUCK: 4,
                       ACTION_SENSE_GOLD: 1,
                       ACTION_MINE_GOLD: 10,
                       ACTION_UNLOAD_GOLD: 1,
                       ACTION_NOP: 1}

class VacuumAgent(Agent):
    def __init__(self, version, log, battery, exec):
        # Agent superclass holds function call to have agent choose next action
        super().__init__(exec)
        # Version is documentation string only
        self.version = version
        # Agent writes log messages by calling this function
        self.log = log
        # Remaining battery units
        self.battery_level = battery
        # Score bonuses and action power consumption
        self._score = 0
        self.action_battery_consumption = BATTERY_CONSUMPTION
        self.dirt_reward = DIRT_REWARD
        self.gold_reward = GOLD_REWARD
        self.battery_depleted_reported = False
        self.num_gold = 0
         
    # Agent must call this on each call every time its execute
    # method is called -- update last action, score, and battery
    # consumption
    
    def step_update(self, action, percept):
        self.battery_level -= self.action_battery_consumption[action]
        self._score += self.action_reward(action, percept)
        
    def action_reward(self, action, percept):
        if (action == ACTION_SUCK and percept.attributes["dirt"]):
            return self.dirt_reward
        else:
            return 0
        
    # This is called by the environment when the agent 
    # successfully unloads some gold.  
    def add_gold_reward(self):
         self._score += self.gold_reward
         
    # Default getter for agent score
    def score(self):
        return self._score
    
            # Standard pattern for dealing with depleted battery -- repeated
        # in all agents
    def battery_depleted(self):  
        if self.battery_level <= 0:
            if not self.battery_depleted_reported:
                self.log("Battery level is now 0. Halting!")
                self.log("Score: {}".format(self.score()))
                self.battery_depleted_reported = True
            return True
        else:
            return False
        
        
        
        
    