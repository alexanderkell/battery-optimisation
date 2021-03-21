from pytest import fixture
import pandas as pd
from pathlib import Path

@fixture
def model():
    from src.models.battery_model import Battery

    return Battery(5000)


def test_charge_battery(model):
    model.use_battery(10)
    assert model.current_charge == 10
    model.use_battery(-5)
    assert model.current_charge == 5
    model.use_battery(0)
    assert model.current_charge == 5
    model.use_battery(-10)
    assert model.current_charge == 0
    model.use_battery(model.battery_size + 500)
    assert model.current_charge == model.battery_size


def test_charge_battery_reward(model):
    assert model.use_battery(5) == 0
    assert model.use_battery(-10) == 5
    assert model.use_battery(model.battery_size + 5000) == 5000


@fixture
def house_system_list():
    from src.models.battery_model import HouseSystemFactory

    project_dir = Path(__file__).resolve().parents[1]
    consumption_data_path = "{}/data/processed/lagged_2012-2013-solar-electricity-data.csv".format(
        project_dir)

    consumption_data = pd.read_csv(
        consumption_data_path,
        nrows=20000
    )

    factory = HouseSystemFactory(battery_size=5000)
    house_system_list = factory.create_house_system(consumption_data)

    return house_system_list


def test_house_system_factory(house_system_list):
    house_system = house_system_list[0]

    assert house_system.customer_number == 1
    assert house_system.generator_capacity == 3.78
    assert house_system.postcode == 2076
    