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
    consumption_data_path = (
        "{}/data/processed/lagged_2012-2013-solar-electricity-data.csv".format(
            project_dir
        )
    )

    consumption_data = pd.read_csv(
        consumption_data_path,
    )

    factory = HouseSystemFactory(battery_size=5000)
    house_system_list = factory.create_house_system(consumption_data)

    return house_system_list


@fixture
def house_system_list_normal_size():
    from src.models.battery_model import HouseSystemFactory

    project_dir = Path(__file__).resolve().parents[1]
    consumption_data_path = (
        "{}/data/processed/lagged_2012-2013-solar-electricity-data.csv".format(
            project_dir
        )
    )

    consumption_data = pd.read_csv(
        consumption_data_path,
    )

    factory = HouseSystemFactory(battery_size=13)
    house_system_list = factory.create_house_system(consumption_data)

    return house_system_list


def test_house_system_factory(house_system_list):
    house_system = house_system_list[0]

    assert house_system.customer_number == 1
    assert house_system.generator_capacity == 3.78
    assert house_system.postcode == 2076

    house_system = house_system_list[-1]
    assert house_system.customer_number == 4
    assert house_system.generator_capacity == 1.00
    assert house_system.postcode == 2220

    assert (
        house_system.controlled_load_consumption["Consumption Category"].iloc[0]
        == "controlled_load_consumption"
    )
    assert (
        house_system.general_electricity_consumption["Consumption Category"].iloc[0]
        == "general_electricity_consumption"
    )
    assert (
        house_system.solar_generation["Consumption Category"].iloc[0]
        == "solar_generation"
    )


def test_service_electricity_load(house_system_list):
    house_system = house_system_list[0]
    (
        residual_general_electricity_consumption,
        residual_controlled_load_consumption,
        residual_battery_energy,
    ) = house_system.service_electricity_load(
        battery_discharge_size=10,
        current_controlled_load_consumption=20,
        current_general_electricity_consumption=0,
    )

    assert residual_controlled_load_consumption == 10
    assert residual_general_electricity_consumption == 0
    assert residual_battery_energy == 0

    (
        residual_general_electricity_consumption,
        residual_controlled_load_consumption,
        residual_battery_energy,
    ) = house_system.service_electricity_load(
        battery_discharge_size=10,
        current_controlled_load_consumption=0,
        current_general_electricity_consumption=20,
    )

    assert residual_controlled_load_consumption == 0
    assert residual_general_electricity_consumption == 10
    assert residual_battery_energy == 0

    (
        residual_general_electricity_consumption,
        residual_controlled_load_consumption,
        residual_battery_energy,
    ) = house_system.service_electricity_load(
        battery_discharge_size=10,
        current_controlled_load_consumption=5,
        current_general_electricity_consumption=0,
    )

    assert residual_controlled_load_consumption == 0
    assert residual_general_electricity_consumption == 0
    assert residual_battery_energy == 5

    (
        residual_general_electricity_consumption,
        residual_controlled_load_consumption,
        residual_battery_energy,
    ) = house_system.service_electricity_load(
        battery_discharge_size=10,
        current_controlled_load_consumption=0,
        current_general_electricity_consumption=5,
    )

    assert residual_controlled_load_consumption == 0
    assert residual_general_electricity_consumption == 0
    assert residual_battery_energy == 5

    (
        residual_general_electricity_consumption,
        residual_controlled_load_consumption,
        residual_battery_energy,
    ) = house_system.service_electricity_load(
        battery_discharge_size=40,
        current_controlled_load_consumption=10,
        current_general_electricity_consumption=5,
    )

    assert residual_controlled_load_consumption == 0
    assert residual_general_electricity_consumption == 0
    assert residual_battery_energy == 25

    (
        residual_general_electricity_consumption,
        residual_controlled_load_consumption,
        residual_battery_energy,
    ) = house_system.service_electricity_load(
        battery_discharge_size=40,
        current_controlled_load_consumption=55,
        current_general_electricity_consumption=0,
    )

    assert residual_controlled_load_consumption == 15
    assert residual_general_electricity_consumption == 0
    assert residual_battery_energy == 0

    (
        residual_general_electricity_consumption,
        residual_controlled_load_consumption,
        residual_battery_energy,
    ) = house_system.service_electricity_load(
        battery_discharge_size=40,
        current_controlled_load_consumption=0,
        current_general_electricity_consumption=55,
    )

    assert residual_controlled_load_consumption == 0
    assert residual_general_electricity_consumption == 15
    assert residual_battery_energy == 0

    (
        residual_general_electricity_consumption,
        residual_controlled_load_consumption,
        residual_battery_energy,
    ) = house_system.service_electricity_load(
        battery_discharge_size=40,
        current_controlled_load_consumption=30,
        current_general_electricity_consumption=30,
    )

    assert residual_controlled_load_consumption == 0
    assert residual_general_electricity_consumption == 20
    assert residual_battery_energy == 0


def test_charge_battery_in_house(house_system_list):
    house_system = house_system_list[0]
    input_energy, current_controlled_load_consumption = house_system.charge_battery(
        charge_solar=1,
        charge_load=1,
        discharge_size=1,
        current_solar=2,
        current_controlled_load_consumption=2,
    )

    assert input_energy == 2
    assert current_controlled_load_consumption == 3
    assert house_system.battery.current_charge == 1


def test_electricity_cost(house_system_list):
    house_system = house_system_list[0]
    step_cost = house_system.electricity_cost(
        general_electricity_consumption=1, controlled_load_consumption=1
    )

    assert step_cost == 0.37

    step_cost = house_system.electricity_cost(
        general_electricity_consumption=10, controlled_load_consumption=10
    )

    assert step_cost == 3.70


def test_house_system_step_normal_battery(house_system_list_normal_size):
    house_system = house_system_list_normal_size[0]
    observations, reward, done, info = house_system.step(
        charge_solar=1, charge_load=1, discharge_size=1
    )

    (
        battery_size,
        current_charge,
        residual_general_electricity_consumption,
        residual_controlled_load_consumption,
        current_solar,
        current_controlled_load_consumption,
        current_general_electricity_consumption,
    ) = observations
    assert battery_size == 13
    assert current_charge == 0
    assert current_solar == 0
    # assert current_controlled_load_consumption == 1.238
    # assert current_general_electricity_consumption == 1.299
    assert done is False
    # assert residual_general_electricity_consumption == 1.299
    # assert reward == -
