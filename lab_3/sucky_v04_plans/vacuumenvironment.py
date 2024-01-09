from random import random, Random, randint
from environment import Environment
from constants import ACTION_FORWARD, ACTION_SUCK, ACTION_UNSUCK, ACTION_TURN_LEFT
from constants import ACTION_TURN_RIGHT, ACTION_NOP, ACTION_SENSE_GOLD, ACTION_MINE_GOLD, ACTION_UNLOAD_GOLD, ACTION_STOP
from constants import DIRT, CLEAN, WALL, GOLD

# Need to communicate heading to the agent / world model in the recon report
from headings import EAST

class Percept:
    def __init__(self, attributes):
        self.attributes = attributes


class VacuumEnvironment(Environment):

    """
    Create a vacuum environment with the given width, height, world-gen element biases and PRF seed
    """
    def __init__(self, env_x=5, env_y=5, dirt_bias=0.1, wall_bias=0.0, gold_bias=0.0, world_seed=None):
        super().__init__()
        self.env_x = env_x
        self.env_y = env_y
        self.dirt_bias = dirt_bias
        self.wall_bias = wall_bias
        self.gold_bias = gold_bias
        self.world = None
        self.randomize_world(world_seed)

    """
    Add thing to environment
    """
    def add_thing(self, thing, location=None):
        thing.facing = (1, 0)
        super().add_thing(thing, location)

    def percept(self, agent):
        return Percept({"home": agent.location[0] == 1 and agent.location[1] == 1,
                        "dirt": self.world[agent.location[0]][agent.location[1]] == DIRT
                        ,
                        "bump": agent.bump})
  
    """
    Process actions generated by agents in environment
    """
    def execute_action(self, agent, action):

        agent.bump = False
    
        if action == ACTION_FORWARD:
            new_location = (agent.location[0] + agent.facing[0], agent.location[1] + agent.facing[1])
            agent.bump = self.world[new_location[0]][new_location[1]] == WALL
            agent.location = agent.location if agent.bump else new_location
        elif action == ACTION_SUCK:
            if self.world[agent.location[0]][agent.location[1]] == DIRT:
                agent.add_dirt_reward()
                self.world[agent.location[0]][agent.location[1]] = CLEAN
                agent.num_dirt += 1
        elif action == ACTION_UNSUCK:
            pass
            #if agent.num_dirt > 0:
            #    agent.num_dirt -= 1
            #    self.world[agent.location[0]][agent.location[1]] = ENV_DIRTY
        elif action == ACTION_TURN_LEFT:
            """
            NORTH -> WEST   |  ( 0, -1) -> (-1,  0)
            EAST  -> NORTH  |  ( 1,  0) -> ( 0, -1)
            SOUTH -> EAST   |  ( 0,  1) -> ( 1,  0)
            WEST  -> SOUTH  |  (-1,  0) -> ( 0,  1)
            """
            agent.facing = (agent.facing[1], -agent.facing[0] if agent.facing[0] != 0 else agent.facing[0])
        elif action == ACTION_TURN_RIGHT:
            agent.facing = (-agent.facing[1] if agent.facing[1] != 0 else agent.facing[1], agent.facing[0])        
        elif action == ACTION_SENSE_GOLD:
            pass
        elif action == ACTION_MINE_GOLD:   
            if self.world[agent.location[0]][agent.location[1]] == GOLD and agent.num_gold < 2:
                    agent.num_gold += 1
                    self.world[agent.location[0]][agent.location[1]] = CLEAN
        elif action == ACTION_UNLOAD_GOLD:
            if agent.location[0] == 1 and agent.location[1] == 1 and agent.num_gold > 0:
                agent.num_gold -= 1
                agent.add_gold_reward()
            elif agent.num_gold > 0:
                agent.num_gold -=1
                self.world[agent.location[0]][agent.location[1]] = GOLD
        elif action == ACTION_NOP:
            pass
        elif action == ACTION_STOP:
            agent.is_alive = False
        else:
            raise(Exception(f"Bad action {action}"))
            
        return True
                    
    """
    Random-generate an environment for the vacuum with an optional seed
    """
    
    def wallify(self, randfunc):
        self.world =  [
                [
                WALL if
                    x == 0 or
                    x == self.env_x - 1 or
                    y == 0 or
                    y == self.env_y - 1 or
                    (randfunc() < self.wall_bias and not (x == 1 and y == 1))
                else CLEAN
                for y in range(self.env_y)
            ]
            for x in range(self.env_x)
        ]
        
    def dirtify(self, randfunc):
        for x in range(self.env_x-1):
            for y in range(self.env_y-1):
                if (self.world[x][y] != WALL):
                    if randfunc() < self.dirt_bias:
                        self.world[x][y] = DIRT
                      
    ''' 
    Old code for more sophisticated gold sensor, where prior is based on 
    quadrant.
    
     def quadrant_for(self, r, c):
            m = int(self.env_x / 2)
            if r < m and c < m:
                return 0
            elif r < m and c >= m:
                return 1
            elif r >= m and c < m:
                return 2
            else:
                return 3
            
        def quadrant_positions(self, quadrant):
            m = int(self.env_x / 2)
            xrange = range(0, m) if quadrant < 2 else range(m, self.env_x)
            yrange = range(0,m) if quadrant == 0 or quadrant == 2 else range(m, self.env_y)
            return [(x, y) for x in xrange for y in yrange]
         
        def quadrant_sum(self, quadrant, state):
            return sum([1 if self.world_pos_state(p) == state else 0 for p in self.quadrant_positions(quadrant)])
        
        def world_pos_state(self, p):
            return self.world[p[0]][p[1]]
    '''
    
    def goldify(self, randfunc):
        if self.gold_bias == int(self.gold_bias):
            self.goldify_by_count()
        else:
            self.goldify_by_bias(randfunc)
  
    def goldify_by_count(self):
        num_gold = self.gold_bias
        while num_gold > 0:
            x = randint(0, self.env_x-1)
            y = randint(0, self.env_y-1)
            if self.world[x][y] not in [DIRT, WALL]:
                self.world[x][y] = GOLD
                num_gold -= 1
                
    def goldify_by_bias(self, randfunc):
        for x in range(self.env_x-1):
            for y in range(self.env_y-1):
                if self.world[x][y] not in [WALL, DIRT]:
                    if randfunc() < self.gold_bias:
                        self.world[x][y] = GOLD        
                
    def randomize_world(self, seed=None):
        randfunc = random if seed is None else Random(seed).random
        self.wallify(randfunc)
        self.dirtify(randfunc)
        self.goldify(randfunc)
    
    # CAUTION!
    #   The position argument is possibly breaking since it's just 
    #   the default place where Things are placed (see defn of default_location)
    
    def prep_agent(self, agent, recon_type):
        if not recon_type in ['None', 'WallsOnly', 'Full', 'WallsAndGold']:
            raise(Exception(f"Bad recon type {recon_type}"))
        recon = {'width': self.env_x,
                 'height': self.env_y,
                 'position': (1,1),
                 'heading': EAST}
        if recon_type == "WallsOnly":
            recon['walls'] = self.env_positions(WALL)
        elif recon_type == "WallsAndGold":
            recon['walls'] =  self.env_positions(WALL)
            recon['gold']  = self.env_positions(GOLD)
        elif recon_type == "Full":
            recon['walls'] =  self.env_positions(WALL)
            recon['gold']  = self.env_positions(GOLD)
            recon['dirt']  =  self.env_positions(DIRT)
        agent.prep(recon)
    
    def env_positions(self, env):
        return [(r,c) for r in range(self.env_y) for c in range(self.env_x) if self.world[c][r] == env]

        
        
   
