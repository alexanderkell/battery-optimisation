import gym, ray
from ray.rllib.agents import ddpg
from pathlib import Path
from src.models.battery_model import HouseSystem, HouseSystemFactory
import pandas as pd
from ray import tune
import ray
from ray.rllib.models import ModelCatalog
from ray.tune import grid_search
from gym.spaces import Box, Discrete, MultiDiscrete
import numpy as np


class BatteryEnv(gym.Env):
    def __init__(self, env_config):

        action_space = Box(low=0, high=10000, shape=(3,), dtype=np.float32)
        observation_space = Box(low=-10000, high=10000, shape=(7,), dtype=np.float32)

        self.observation_space = observation_space
        self.action_space = action_space

        project_dir = Path(__file__).resolve().parents[2]
        consumption_data_path = "{}/data/processed/lagged_2012-2013-solar-electricity-data.csv".format(
            project_dir)

        consumption_data = pd.read_csv(
            consumption_data_path,
        )

        factory = HouseSystemFactory(battery_size=5000)
        house_system_list = factory.create_house_system(consumption_data)
        
        self.house_system = house_system_list[0]

        self.start_obs = [
            self.house_system.battery.battery_size,
            self.house_system.battery.current_charge,
            0,
            0,
            0,
            0,
            0
        ]

    def reset(self):


        return self.start_obs

    def step(self, action):
        observations, reward, done, info = self.house_system.step(action[0], action[1], action[2])

        if isinstance(reward, np.ndarray):
            if reward.size == 0:
                reward = 0
            else:
                reward = reward[0]

        if isinstance(observations[2], np.ndarray):
            if observations[2].size == 0:
                observations = self.start_obs
        return observations, reward, done, info


ray.init()
# ModelCatalog.register_custom_model("battery_env")
        
config = {
    "env": BatteryEnv, 
    "lr": grid_search([1e-2]),  # try different lrs
    "num_workers": 1,  # parallelism
}

stop = {
    "training_iteration": 1000,
}

results = tune.run("DDPG", config=config, stop=stop)

# if args.as_test:
#     check_learning_achieved(results, args.stop_reward)
# ray.shutdown()