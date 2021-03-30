# from src.models.rollout import run
import subprocess
from pathlib import Path


def call_rollout(directory, battery_size):
    subprocess.call(
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
            '{"env_config":{"battery_size": ' + str(battery_size) + "}}",
        ]
    )


if __name__ == "__main__":

    # call_rollout("1.4")
    p = Path(
        "/Users/alexanderkell/Documents/PhD/Projects/18-battery-optimisation/data/models"
    )
    subdirectories = [
        "{}/checkpoint_30/checkpoint-30".format(x) for x in p.iterdir() if x.is_dir()
    ]

    battery_sizes = [
        directory.split("_battery_size=")[1].split(",")[0]
        for directory in subdirectories
    ]

    for directory, battery_size in zip(subdirectories, battery_sizes):
        call_rollout(directory, battery_size)
