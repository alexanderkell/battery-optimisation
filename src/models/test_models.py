# from src.models.rollout import run
from subprocess import Popen, PIPE
from pathlib import Path
import pickle


def call_rollout(directory, battery_size):
    p = Popen(
        [
            "/Users/alexanderkell/anaconda3/envs/battery-optimisation/bin/python",
            "src/models/rollout.py",
            directory,
            "--run",
            "DDPG",
            "--env",
            "BatteryEnv",
            "--episodes",
            "2",
            "--no-render",
            "--config",
            '{"env_config":{"battery_size": '
            + str(battery_size)
            + ', "consumption_data":"/data/processed/train_full_weeks.csv"}}',
        ],
        stdout=PIPE,
    )
    output = p.stdout.read()

    return output


if __name__ == "__main__":

    rewards = {"battery_size": [], "reward": [], "directory": []}
    p = Path(
        "/Users/alexanderkell/Documents/PhD/Projects/18-battery-optimisation/data/models/new"
    )
    subdirectories = [
        "{}/checkpoint_30/checkpoint-30".format(x) for x in p.iterdir() if x.is_dir()
    ]

    battery_sizes = [
        directory.split("_battery_size=")[1].split("_")[0]
        for directory in subdirectories
    ]

    for directory, battery_size in zip(subdirectories, battery_sizes):
        reward = call_rollout(directory, battery_size)
        rewards["battery_size"].append(battery_size)
        rewards["directory"].append(directory)
        rewards["reward"].append(reward)

    print("rewards: {}".format(rewards))
    with open(
        "/Users/alexanderkell/Documents/PhD/Projects/18-battery-optimisation/data/results/testing/rewards.pickle",
        "wb",
    ) as handle:
        pickle.dump(rewards, handle, protocol=pickle.HIGHEST_PROTOCOL)
