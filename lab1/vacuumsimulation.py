# -*- coding: utf-8 -*-
from lab1.liuvacuum import LIUVacuumEnvironment

from lab1.v1agent import V1Agent
from lab1.v2agent import V2Agent
from lab1.v3agent import V3Agent
from lab1.v4agent import V4Agent
from lab1.v5agent import V5Agent
from lab1.v6agent import V6Agent

from random import randint

from lab1.liuvacuum import ACTION_NOP

def log_to_console(msg):
    print(msg)

def log_null(msg):
    pass

class VacuumSimulation:
    def __init__(self, agent, dirt_bias, wall_bias, world_seed):
        self.env = LIUVacuumEnvironment(env_x=20, 
                                        env_y=20, 
                                        dirt_bias=dirt_bias,
                                        dirt_distribution = 0.0,
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
# Iterate many times:
#   Create a 

def run_agents_in_environment(agents, 
                              dirt_density, 
                              wall_density, 
                              num_samples = 100, 
                              output_file_name = 'simulation_results.csv',
                              print_results_to_console = False):
    with open(output_file_name, 'w') as output_file:
        for i in range(1, num_samples):
            seed = randint(1,10000)
            for a in agents:
                v = VacuumSimulation(a, dirt_density, wall_density, seed)
                v.run()
                output_file.write(f"{a.version},{dirt_density},{wall_density},{a.score()}\n")
                if print_results_to_console:
                    print(f"{a.version},{dirt_density},{wall_density},{a.score()}")


#######################################
                    
agents = [#V1Agent(20, 20, log_null, 300), 
          #V2Agent(20, 20, log_null, 300),
          V3Agent(20, 20, log_null, 300),
          V4Agent(20, 20, log_null, 300),
          #V5Agent(20, 20, log_null, 300),
          #V6Agent(20, 20, log_null, 300),
          ]


dirt_density = 0.3
wall_density = 0.3
output_file_name = 'simulation_results.csv'

run_agents_in_environment(agents, dirt_density, wall_density, 100, output_file_name, True)
