# app.py
import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from gym import spaces

# Define Forex Trading Environment (same as in train.py)
class ForexTradingEnv:
    def __init__(self, data, initial_balance=1000):
        self.data = data
        self.initial_balance = initial_balance
        self.current_step = 0
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(3,), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        self.balance = self.initial_balance
        self.position = 0
        self.net_worth = self.balance
        return np.array([self.data['Close'][self.current_step], self.balance, self.position])

    def step(self, action):
        self.current_step += 1
        if self.current_step >= len(self.data) - 1:
            self.current_step = 0
        
        prev_balance = self.balance
        prev_position = self.position
        price = self.data['Close'][self.current_step]
        
        if action == 1:  # Buy
            if self.position == 0:
                self.position = 1
                self.balance -= price
        elif action == 2:  # Sell
            if self.position == 1:
                self.position = 0
                self.balance += price

        reward = self.balance - prev_balance
        done = False
        if self.current_step == len(self.data) - 1:
            done = True

        self.net_worth = self.balance + (self.position * price)
        info = {}

        return np.array([price, self.balance, self.position]), reward, done, info

# Load the trained model
model = tf.keras.models.load_model('dqn_forex_trading_model.h5')

# Create Streamlit interface
st.title('AI Forex Trading Bot')

# Load Forex data
data = pd.read_csv('forex_data.csv')

# Initialize environment
env = ForexTradingEnv(data)
state = np.array([data['Close'][0], 1000, 0])  # Start state

# Displaying Forex data
st.subheader("Forex Data")
st.write(data)

# Action selection and simulation
action = st.selectbox('Select Action', ['Hold', 'Buy', 'Sell'])

if action == 'Buy':
    action = 1
elif action == 'Sell':
    action = 2
else:
    action = 0

# Get the next step in the environment
next_state, reward, done, _ = env.step(action)

st.write(f"Action selected: {action}")
st.write(f"Current Price: {data['Close'][env.current_step]}")
st.write(f"Next State: {next_state}")
st.write(f"Reward: {reward}")
