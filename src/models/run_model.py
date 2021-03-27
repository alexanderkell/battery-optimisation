import gym
from pathlib import Path
from src.models.battery_model import HouseSystemFactory
import pandas as pd
from ray import tune
import ray
from ray.tune import grid_search
from gym.spaces import Box, Discrete, MultiDiscrete
import numpy as np
import math
from ray.tune import grid_search


class BatteryEnv(gym.Env):
    def __init__(self, env_config):
        print("env_config: {}".format(env_config))
        self.battery_size = env_config["battery_size"]
        self.setup_environment(self.battery_size)

    def reset(self):
        self.setup_environment(self.battery_size)
        return self.start_obs

    def step(self, action):
        observations, reward, done, info = self.house_system.step(
            action[0], action[1], action[2]
        )

        return observations, reward, done, info

    def setup_environment(self, battery_size):

        action_space = Box(low=0, high=battery_size, shape=(3,), dtype=np.float32)
        observation_space = Box(low=-1000, high=1000, shape=(7,), dtype=np.float32)

        self.observation_space = observation_space
        self.action_space = action_space

        project_dir = Path(__file__).resolve().parents[2]
        consumption_data_path = (
            "{}/data/processed/lagged_2012-2013-solar-electricity-data.csv".format(
                project_dir
            )
        )

        consumption_data = pd.read_csv(
            consumption_data_path,
        )

        factory = HouseSystemFactory(battery_size=battery_size)
        house_system_list = factory.create_house_system(consumption_data)
        self.house_system = house_system_list[0]

        self.start_obs = [
            self.house_system.battery.battery_size,
            self.house_system.battery.current_charge,
            0,
            0,
            0,
            0,
            0,
        ]


ray.init()

config = {
    "env": BatteryEnv,
    "lr": grid_search([1e-2]),  # try different lrs
    "num_workers": 4,  # parallelism
    "env_config": {"battery_size": grid_search([3, 5, 10, 15])},
}

stop = {
    # "training_iteration": 1000,
}

results = tune.run("DDPG", config=config, stop=stop)
