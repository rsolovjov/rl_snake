import gymnasium as gym
from gymnasium import spaces
from types import SimpleNamespace
import numpy as np
from snake_game import Snake
import math

class SnakeCnnEnv(gym.Env): 
    def __init__(self):
        super().__init__()
        
        self.game = Snake(36, 14)
        
        state = self.game.reset()
        state = SimpleNamespace(**state)
        
        self.prev_length = state.length
        self.prev_head = state.head
        
        self.observation_space = spaces.Box(low=0, high=255, shape=(1, state.board_size, state.board_size), dtype=np.uint8)
        self.action_space = spaces.Discrete(4)
        
        self.game.init_render()
    
        self.reward_range = (-1, 1)
        
    def step(self, action):
        #print(action)
        state = self.game.step(action)
        state = SimpleNamespace(**state)
        
        length_diff = state.length - self.prev_length
        
        reward = 0
        if state.game_over:
            if state.win:
                reward = 1
            else:
                reward = -1
        else:
            if length_diff > 0:
                reward = 1    
            else:
                prev_distance = math.sqrt( (state.food[0] - self.prev_head[0]) ** 2 + (state.food[1] - self.prev_head[1]) ** 2)
                new_distance  = math.sqrt( (state.food[0] - state.head[0]) ** 2     + (state.food[1] - state.head[1]) ** 2)
                if new_distance < prev_distance:
                    reward = 0.01
                else:
                    reward = -0.02
            
        self.prev_length = state.length
        self.prev_head = state.head
        
        board_map = np.reshape(state.board, (1, state.board_size, state.board_size))

        return board_map, reward, state.game_over, state.trunc, {}
    
    def reset(self, seed=0):
        # Return the first frame 
        state = self.game.reset()
        state = SimpleNamespace(**state)
        
        self.prev_length = state.length
        self.prev_head = state.head
        
        board_map = np.reshape(state.board, (1, state.board_size, state.board_size))
        return board_map, {}
    
    def render(self):
        self.game.render()