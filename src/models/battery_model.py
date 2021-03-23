from datetime import datetime, timedelta
import pandas as pd


class Battery:

    def __init__(self, battery_size=5000):
        self.battery_size = battery_size
        self.current_charge = 0

    def use_battery(self, energy):
        if energy > 0:
            residual = self.charge(energy)
            return residual
        elif energy < 0:
            residual = self.discharge(energy)
            return residual
        else: 
            return 0

    def charge(self, charge_size):
        if self.current_charge + charge_size < self.battery_size:
            self.current_charge += charge_size
            return 0
        else:
            residual_energy = self.battery_size - self.current_charge
            self.current_charge = self.battery_size
            return residual_energy

    def discharge(self, discharge_size):
        if self.current_charge >= - discharge_size:
            self.current_charge += discharge_size
            return - discharge_size
        elif self.current_charge < - discharge_size:
            residual_energy = self.current_charge + discharge_size
            self.current_charge = 0
            return - residual_energy
        else:
            return 0

    def is_battery_full(self):
        if self.current_charge == self.battery_size:
            return True
        else:
            return False


class HouseSystemFactory():
    def __init__(self, battery_size):
        self.battery_size = battery_size

    def create_house_system(self, input, single_rate_tariff=27, controlled_load_tariff=10):
        if isinstance(input, pd.DataFrame):

            house_system_list = []
            for (customer_number, generator_capacity, postcode), data in input.groupby(["Customer", "Generator Capacity", "Postcode"]):
                solar_generation = data[data['Consumption Category']
                                        == "solar_generation"]
                controlled_load_consumption = data[data['Consumption Category']
                                                   == "controlled_load_consumption"]
                general_electricity_consumption = data[data['Consumption Category']
                                                       == "general_electricity_consumption"]

                house_system = HouseSystem(
                    self.battery_size,
                    customer_number,
                    generator_capacity,
                    postcode,
                    solar_generation,
                    controlled_load_consumption,
                    general_electricity_consumption,
                    single_rate_tariff,
                    controlled_load_tariff
                )
                house_system_list.append(house_system)
            return house_system_list


class HouseSystem:
    # tariff data: https://www.canstarblue.com.au/electricity/controlled-load-tariff-can-save-money/
    def __init__(self, battery_size, customer_number, generator_capacity, postcode, solar_generation, controlled_load_consumption, general_electricity_consumption, single_rate_tariff=27, controlled_load_tariff=10):
        self.battery_size = battery_size
        self.battery = Battery(battery_size)
        self.customer_number = customer_number
        self.generator_capacity = generator_capacity
        self.postcode = postcode
        self.solar_generation = solar_generation
        self.controlled_load_consumption = controlled_load_consumption
        self.general_electricity_consumption = general_electricity_consumption
        self.single_rate_tariff = single_rate_tariff
        self.controlled_load_tariff = controlled_load_tariff
        self.datetime = datetime(2012, 1, 8, 0, 30)

        self.time_step = timedelta(minutes=30)

    def step(self, charge_solar, charge_load, discharge_size):
        self.datetime += self.time_step
        current_solar = self.solar_generation[self.solar_generation.datetime == str(self.datetime)].consumption.values
        current_controlled_load_consumption = self.controlled_load_consumption[self.controlled_load_consumption.datetime == str(self.datetime)].consumption.values
        current_general_electricity_consumption = self.general_electricity_consumption[self.general_electricity_consumption.datetime == str(self.datetime)].consumption.values
        
        # charge battery with solar or load
        input_energy, current_general_electricity_consumption = self.charge_battery(charge_solar, charge_load, discharge_size, current_solar, current_general_electricity_consumption)

        self.battery.use_battery(-discharge_size)

        # discharge battery
        residual_general_electricity_consumption, residual_controlled_load_consumption, residual_battery_energy = self.service_electricity_load(
            input_energy, current_controlled_load_consumption, current_general_electricity_consumption)

        self.battery.use_battery(residual_battery_energy)

        # Service rest of the load with tariff
        cost = self.electricity_cost(
            residual_general_electricity_consumption, residual_controlled_load_consumption)
        reward = -cost
        done = True if self.datetime == datetime(
            2013, 12, 6, 23, 30) else False

        observations = [
            self.battery.battery_size,
            self.battery.current_charge,
            residual_general_electricity_consumption,
            residual_controlled_load_consumption,
            current_solar,
            current_controlled_load_consumption,
            current_general_electricity_consumption
        ]

        return observations, reward, done, {}

    def charge_battery(self, charge_solar, charge_load, discharge_size, current_solar, current_general_electricity_consumption):
        residual_battery_solar = self.battery.use_battery(charge_solar)
        current_solar -= (charge_solar - residual_battery_solar)

        residual_battery_load = self.battery.use_battery(charge_load)
        current_general_electricity_consumption += (charge_load - residual_battery_load)

        input_energy = residual_battery_solar + residual_battery_load + current_solar + discharge_size
        return input_energy, current_general_electricity_consumption

    def service_electricity_load(self, battery_discharge_size, current_controlled_load_consumption, current_general_electricity_consumption):
        residual_controlled_load_consumption = current_controlled_load_consumption
        residual_general_electricity_consumption = current_general_electricity_consumption
        residual_battery_energy = battery_discharge_size

        if residual_battery_energy > 0:
            if current_controlled_load_consumption > 0:
                if residual_battery_energy < current_controlled_load_consumption:
                    residual_controlled_load_consumption = current_controlled_load_consumption - \
                        residual_battery_energy
                    residual_battery_energy = 0
                else:
                    residual_controlled_load_consumption = 0
                    residual_battery_energy -= current_controlled_load_consumption
                
            if current_general_electricity_consumption > 0 and residual_battery_energy > 0:
                if residual_battery_energy < current_general_electricity_consumption:
                    residual_general_electricity_consumption = current_general_electricity_consumption - \
                        residual_battery_energy
                    residual_battery_energy = 0
                else:
                    residual_general_electricity_consumption = 0
                    residual_battery_energy -= current_general_electricity_consumption

        return residual_general_electricity_consumption, residual_controlled_load_consumption, residual_battery_energy

    def electricity_cost(self, general_electricity_consumption, controlled_load_consumption):
        general_consumption_cost = self.single_rate_tariff * general_electricity_consumption
        controlled_consumption_cost = self.controlled_load_tariff * \
            controlled_load_consumption

        step_cost = general_consumption_cost + controlled_consumption_cost
        return step_cost
