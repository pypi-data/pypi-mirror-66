import gym
from gym import spaces
import numpy as np

class ContinuousGridWorldEnv(gym.Env):
    def __init__(self, width, height, max_step, goal_x, goal_y, goal_side):

        self.width = width
        self.height = height
        self.max_step = max_step
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.goal_side = goal_side

        obs_low = np.array([0., 0.], dtype=np.float32)
        obs_high = np.array([width, height], dtype=np.float32)
        act_high = np.array([max_step, max_step])
        self.action_space = spaces.Box(low=-act_high, high=act_high, dtype=np.float32)
        self.observation_space = spaces.Box(low=-obs_low, high=obs_high, dtype=np.float32)

    def step(self, action):
        action = np.clip(action, -self.max_step, self.max_step).reshape(self.state.shape)
        self.state += action

        self.state = np.clip(self.state, self.observation_space.low, self.observation_space.high)
        reward = 0

        if self.in_box():
            reward = 1

        done = True if reward else False

        return self.state, np.array([reward]), done, {}

    def reset(self):
        high = np.array([self.width, self.height])
        self.state = self.observation_space.sample()
        return self.state

    def render(self, mode='human', close=False):
        print(f'state: {self.state}')

    def in_box(self):
        x, y = self.state

        return ((x >= self.goal_x and x <= (self.goal_x + self.goal_side))
                and (y >= self.goal_y and y <= (self.goal_y + self.goal_side)))
