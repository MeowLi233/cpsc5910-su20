from venv.agents.vacuumagent import VacuumAgent
from venv.liuvacuum import ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_FORWARD
from venv.liuvacuum import ACTION_SUCK, ACTION_NOP
from venv.liuvacuum import ACTION_MINE_GOLD, ACTION_UNLOAD_GOLD
from venv.agents.agentworldmodel import AgentWorldModel
from venv.agents.agentworldmodel import NORTH, SOUTH, WEST, EAST
from venv.agents.agentworldmodel import GOLD, DIRT, WALL
from venv.agents.shortestpath import shortest_path


"""
search1

Development version for first exercise:  get complete information about 
walls, dirt, and gold.

"""
VERSION = "S1"

class Search1Agent(VacuumAgent):
    
    def __init__(self, log, battery=500):
        super().__init__(VERSION, log, battery, self.execute)
        self.last_action = None
        self.state = AgentWorldModel(20, 20)
        self.path = []
        self.next_actions = []
        self.count = 0
        self.return_home_low_battery = False
        self.completed = False

    ################################################
    # This method gets called once prior to execution, w/ info about
    # the world.  Just pass it on to the world model
    
    def prep(self, recon):
        self.state.prep(recon)
        self.log("Received recon report, ready to go!")
        self.log(f"Gold: {len(self.state.squares_with_state(GOLD))}," +
                          f" Dirt: {len(self.state.squares_with_state(DIRT))}" +
                          f" Walls: {len(self.state.squares_with_state(WALL))}")
    

   #################################################################
   #  Called once per simulation cycle.  Must return an action choice
     
    def execute(self, percept): 
        
        # Display status periodically
        if self.count % 50 == 0:
            self.log(f"Status:  score={self.score()}  battery={self.battery_level}")
        self.count += 1
        
        # Update world model
        self.state.update(percept.attributes["dirt"], percept.attributes["bump"])
        
        # Choose action
        action = self.choose_action()
 
        # Notify superclass to update score and battery usage
        self.step_update(action, percept)
        self.state.update_action(action)
        
        return action
   
    ###############################################################
    
    def choose_action(self):
        action = None
        
        if self.battery_depleted():
            self.log("Battery depleted")
            action = ACTION_NOP
            
        elif len(self.next_actions) > 0:
            action = self.next_actions.pop(0)
            
        elif self.state.current_position == (1,1) and self.state.num_golds > 0:
            action = ACTION_UNLOAD_GOLD
            self.log(f"Unloading gold ({self.state.num_golds})")
            
        elif self.return_home_low_battery:
            if self.state.current_position == (1,1):
                if not self.completed:
                    self.log(f"Arrived home, DONE!;  score is {self.score()}; total actions {self.state.total_actions}")
                    self.completed = True
                action =  ACTION_NOP
            else:
                action = self.continue_path()
                
        elif self.battery_low():
            self.return_home_low_battery = True
            if self.state.current_position == (1,1):
                action = ACTION_NOP
            else: 
                action = self.go_home()
                self.log(f"Going home with low battery")
                
        elif self.state.current_position in self.state.squares_with_state(DIRT):
            action = ACTION_SUCK
            self.log(f"Sucking dirt")
            
        elif len(self.path) > 0:
            action = self.continue_path()
            
        elif self.state.num_golds >= 2:
            action = self.go_home()
            self.log(f"Going home to unload gold ({self.state.num_golds})")
            
        elif self.state.current_position in self.state.squares_with_state(GOLD)\
                and self.state.num_golds < 2:
            action = ACTION_MINE_GOLD
            self.log(f"Mining gold")
            
        else:
            gold_path = self.path_to(GOLD)
            if gold_path:
                self.log(f"Going for gold at {gold_path[-1]}")
                action = self.begin_path(gold_path)
            else:
                dirt_path = self.path_to(DIRT)
                if dirt_path:
                    self.log(f"Going for dirt at {dirt_path[-1]}")
                    action = self.begin_path(dirt_path)
                elif self.state.current_position == (1,1):
                    if not self.completed:
                        self.completed = True
                        self.log(f"Staying home with nothing to do;  score is {self.score()}; total actions {self.state.total_actions}")
                        return ACTION_NOP
                else:
                    action = self.go_home()
                    self.log(f"Going home with nothing to do!")           
        return action
    
    def battery_low(self):
        return self.battery_level < 3 * len(self.path_home())
    
    ###########################################################
    #  A path is a sequence of positions whose first element
    #   must be the agent's current position.  To follow a path
    #   is to move the agent to the first element in the path,
    #   then remove the first element and then continue to follow
    
    def begin_path(self, path):
        # Edge case where agent asks for a path to where it is currently
        # located
        if len(path) == 0:
            self.path = []
            return ACTION_NOP
        firstpos = path.pop(0)
        self.path = path
        return self.move_to_position(firstpos)
    
    def continue_path(self):
        if len(self.path) == 0:
            return ACTION_NOP
        else:
            return self.move_to_position(self.path.pop(0))
    
    ##################################
    #  Move to an adjacent position.  Depending
    #  on where the position is and the agent's current heading,
    #  this could be FORWARD, or one or two turns followed by FORWARD.
    #
    #  We can queue up all three actions by putting the second and 
    #  third actions on the next_actions list, then they will be
    #  executed next with highest priority in subsequent execute
    #  cycles
    
    def move_to_position(self, pos):
        new_heading = self.heading_for_position(pos)
        action = None
        if self.state.heading == new_heading:
            action = ACTION_FORWARD
        elif (self.state.heading, new_heading) in [(NORTH, EAST), (EAST, SOUTH), (SOUTH, WEST), (WEST, NORTH)]:
            self.next_actions = [ACTION_FORWARD]
            action =  ACTION_TURN_RIGHT
        elif (self.state.heading, new_heading) in [(NORTH, WEST), (WEST, SOUTH), (SOUTH, EAST), (EAST, NORTH)]:
            self.next_actions = [ACTION_FORWARD]
            action =  ACTION_TURN_LEFT
        else:
            self.next_actions = [ACTION_TURN_LEFT, ACTION_FORWARD]
            action = ACTION_TURN_LEFT
        return action

    def heading_for_position(self, new_position):
        my_position = self.state.current_position
        if (my_position[0] < new_position[0]):
            return SOUTH
        elif (my_position[0] > new_position[0]):
            return NORTH
        elif (my_position[1] < new_position[1]):
            return EAST
        elif (my_position[1] > new_position[1]):
            return WEST 
        else:
            raise(Exception("Bad argument to heading_for_position"))
    
    ###################################################################
    #  Finding paths to a square (might be home, might be a square containing
    #  dirt or gold)
 
    # Going home is different from trying to go to a GOLD or DIRT
    # because we know a path exists
    
    def go_home(self):
        self.going_home = True
        return self.begin_path(self.path_home())
    
    def path_home(self):
        return shortest_path(self.state.current_position, 
                             (1,1), 
                             self.state.squares_without_walls())
        
    def path_to(self, object_type):
        best_path = None
        nowall = self.state.squares_without_walls()
        for square in self.state.squares_with_state(object_type):
            p = shortest_path(self.state.current_position, square, nowall)
            if p and (best_path == None or len(p) < len(best_path)):
                best_path = p
        return best_path
            
            
 
    
        