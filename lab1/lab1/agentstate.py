# -*- coding: utf-8 -*-
from lab1.liuvacuum import ACTION_FORWARD, ACTION_SUCK, ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_NOP

UNKNOWN = "Unknown"
WALL = "Wall"
EDGE = "Edge"
CLEAN = "Clean"
DIRT = "Dirt"

# Heading
NORTH = "North"
EAST  = "East"
SOUTH = "South"
WEST = "West"

# Direction (turn)
FORWARD = "Forward"
LEFT = "Left"
RIGHT = "Right"

"""
Internal state of a vacuum agent
"""
class AgentState:

    def __init__(self, width, height, pos_x, pos_y, heading):

        self.world = [[UNKNOWN for _ in range(height)] for _ in range(width)]
        self.last_action = ACTION_NOP
        self.heading = heading
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
    
    def update_action(self, action):
        self.last_action = action
    
    def update(self, dirt, bump):
        if self.last_action == ACTION_NOP:
            self.world[self.pos_x][self.pos_y] =  DIRT if dirt else CLEAN
        elif self.last_action == ACTION_SUCK:
            self.world[self.pos_x][self.pos_y] =  CLEAN
        elif self.last_action == ACTION_TURN_LEFT:
            self.update_heading(LEFT)
        elif self.last_action == ACTION_TURN_RIGHT:
            self.update_heading(RIGHT)
        elif self.last_action == ACTION_FORWARD:
            self.move(dirt, bump)
        else:
            raise(Exception(f"Bad last action {self.last_action}"))
            
    def update_heading(self, direction):
        if direction == LEFT:
            self.heading = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST:NORTH}[self.heading]
        elif direction == RIGHT:
            self.heading = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST:NORTH}[self.heading]
        else:
            raise(f"Bad turn direction: {direction}")
            
    def move(self, dirt, bump):
        (new_x, new_y) = self.new_position(self.pos_x, self.pos_y, self.heading)
        if bump:
            if not self.boundary(new_x, new_y):
                self.world[new_x][new_y] = WALL
        else:
            self.pos_x = new_x
            self.pos_y = new_y
            self.world[new_x][new_y] = DIRT if dirt else CLEAN
                
    def new_position(self, x, y, heading):
        new_x = {NORTH: x-1, SOUTH: x+1, WEST: x, EAST: x}[heading]
        new_y = {NORTH: y, SOUTH: y, WEST: y - 1, EAST: y + 1}[heading]
        return (new_x, new_y)
    
    def boundary(self, x, y):
        b = x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1
        return b
  
    def inbounds(self, x, y):
        return x > 0 and x < self.width-1 and y > 0 and y < self.height - 1
    
    def state_at(self, x, y):
        if self.boundary(x, y):
            return EDGE
        elif not self.inbounds(x, y):
            raise(f"Invalid coordinate {x} {y}")
        else:
            return self.world[x][y]

    def state(self):
        return self.state_at(self.pos_x, self.pos_y)
    
    def heading_in_direction(self, direction):
        if direction == FORWARD:
            return self.heading
        elif direction == LEFT:
            return {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}[self.heading]
        elif direction == RIGHT:
            return {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}[self.heading]
        else:
            raise (f"Bad direction {direction}")
    
    def state_in_direction(self, direction):
        new_heading = self.heading_in_direction(direction)
        (new_x, new_y) = self.new_position(self.pos_x, self.pos_y, new_heading)
        return self.state_at(new_x, new_y)
    
    def state_forward(self):
        return self.state_in_direction(FORWARD)

 