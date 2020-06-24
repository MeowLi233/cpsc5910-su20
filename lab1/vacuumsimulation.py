# -*- coding: utf-8 -*-
from lab1.liuvacuum import LIUVacuumEnvironment

from lab1.v1agent import V1Agent
from lab1.v2agent import V2Agent
from lab1.v3agent import V3Agent
from lab1.v4agent import V4Agent
from lab1.v5agent import V5Agent
from lab1.v6agent import V6Agent
from lab1.v7agent import V7Agent


from lab1.liuvacuum import ACTION_NOP

def log_to_console(msg):
    print(msg)

def log_null(msg):
    pass

class VacuumSimulation:
    def __init__(self, agent, dirt_bias, dirt_distribution, wall_bias, world_seed):
        self.env = LIUVacuumEnvironment(env_x=20, 
                                        env_y=20, 
                                        dirt_bias=dirt_bias, 
                                        dirt_distribution=dirt_distribution, 
                                        wall_bias=wall_bias, 
                                        world_seed=world_seed)

        self.agent = agent
        self.env.add_thing(self.agent)
    
    def step(self):
        self.env.step()
    
    def run(self):
        while True:
            self.step()
            if self.agent.last_action == ACTION_NOP:
                return
    
    def score(self):
        return self.agent.score()

#########################
### This runs the same simulation on seven different agents.

agents = [V1Agent(20, 20, log_null, 300), 
          V2Agent(20, 20, log_null, 300),
          V3Agent(20, 20, log_null, 300),
          V4Agent(20, 20, log_null, 300),
          V5Agent(20, 20, log_null, 300),
          V6Agent(20, 20, log_null, 300),
          V7Agent(20, 20, log_null, 300),
          ]


dirt_density = 0.2
dirt_uniformity = 0
wall_density = 0.1
random_seed = 12321

output_file = 'simulation_results.csv'
with open(output_file, 'w') as of:
    for a in agents:
        v = VacuumSimulation(a, dirt_density, dirt_uniformity, wall_density, random_seed)
        v.run()
        of.write(f"{a.version},{dirt_density},{dirt_uniformity},{wall_density},{a.score()}\n")
