# -*- coding: utf-8 -*-
"""Welcome To Colab

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/notebooks/intro.ipynb
"""

import gym
import numpy as np
import pandas as pd
from gym import spaces

class ForexTradingEnv(gym.Env):
    def __init__(self, data_path):
        super(ForexTradingEnv, self).__init__()
        self.data = pd.read_csv(data_path)
        self.current_step = 0
        self.balance = 100000  # Updated Initial Balance
        self.positions = []

        self.action_space = spaces.Discrete(3)  # Buy, Sell, Hold
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        self.balance = 100000  # Ensure reset balance is also updated
        self.positions = []
        return self._next_observation()

    def step(self, action):
        # Implement Trading Logic
        self.current_step += 1
        done = self.current_step >= len(self.data) - 1
        reward = np.random.randn()  # Placeholder for reward function
        obs = self._next_observation()
        return obs, reward, done, {}

    def _next_observation(self):
        return np.array(self.data.iloc[self.current_step, 1:6])