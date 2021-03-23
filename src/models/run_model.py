import gym, ray
from ray.rllib.agents import ddpg
from pathlib import Path
from src.models.battery_model import HouseSystem, HouseSystemFactory
import pandas as pd
from ray import tune
import ray
from ray.rllib.models import ModelCatalog
from ray.tune import grid_search


class BatteryEnv(gym.Env):
    def __init__(self, env_config):

        project_dir = Path(__file__).resolve().parents[2]
        consumption_data_path = "{}/data/processed/lagged_2012-2013-solar-electricity-data.csv".format(
            project_dir)

        consumption_data = pd.read_csv(
            consumption_data_path,
        )

        factory = HouseSystemFactory(battery_size=5000)
        house_system_list = factory.create_house_system(consumption_data)
        self.house_system = house_system_list[0]

    def reset(self):
        obs = [
            self.house_system.battery.battery_size,
            self.house_system.battery.current_charge,
            0,
            0,
            0,
            0,
            0
        ]

        return obs

    def step(self, action):
        observations, reward, done = self.house_system.step(action[0], action[1], action[2])
        # return <obs>, <reward: float>, <done: bool>
        return observations, reward, done


ray.init()
# ModelCatalog.register_custom_model("battery_env")
        
config = {
    "env": BatteryEnv, 
    "lr": grid_search([1e-2, 1e-4, 1e-6]),  # try different lrs
    "num_workers": 1,  # parallelism
}

stop = {
    "training_iteration": 1000,
}

results = tune.run("PPO", config=config, stop=stop)

# if args.as_test:
#     check_learning_achieved(results, args.stop_reward)
# ray.shutdown()