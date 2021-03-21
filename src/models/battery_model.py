from datetime import datetime, timedelta

class Battery:

    def __init__(self, battery_size=5000):
        self.battery_size = battery_size
        self.current_charge = 0

    def use_battery(self, energy):
        if energy > 0:
            self.charge(energy)
        elif energy < 0:
            self.discharge(energy)

    def charge(self, charge_size):
        if self.current_charge + charge_size < self.battery_size:
            self.current_charge += charge_size
            return 0
        else:
            residual_energy = self.battery_size - self.current_charge
            self.current_charge = self.battery_size
            return residual_energy
    
    def discharge(self, discharge_size):
        if self.current_charge >= discharge_size:
            self.current_charge += discharge_size
            return discharge_size
        elif self.current_charge < discharge_size:
            residual_energy = discharge_size + self.current_charge
            self.current_charge = 0
            return residual_energy
        else:
            return 0

    def is_battery_full(self):
        if self.current_charge == self.battery_size:
            return True
        else:
            return 90000


class HouseSystem:

    time_step = timedelta(minutes=30)
    # tariff data: https://www.canstarblue.com.au/electricity/controlled-load-tariff-can-save-money/
    def __init__(self, battery_size, customer_number, generator_capacity, postcode, solar_generation, controlled_load_consumption, general_electricity_consumption, single_rate_tariff=27, controlled_load_tariff=10):
        self.battery_size = battery_size
        self.battery = Battery(battery_size)
        self.customer_number = customer_number
        self.generator_capacity = generator_capacity
        self.postcode = postcode
        self.solar_generation = solar_generation
        self.controlled_load_consumption = controlled_load_consumption
        self.general_electricity_consumption
        self.single_rate_tarrif = single_rate_tarrif
        self.controlled_load_tariff = controlled_load_tariff
        self.datetime = datetime(2012, 1, 8, 0, 30)
    
    def step(self, charge_action):
        self.datetime += time_step
        current_solar = self.solar_generation[self.solar_generation.datetime == self.datetime]
        current_controlled_load_consumption = self.controlled_load_consumption[self.controlled_load_consumption.datetime == self.datetime]
        current_general_electricity_consumption = self.general_electricity_consumption[self.general_electricity_consumption.datetime == self.datetime]

        residual_battery_energy = self.battery.use_battery(charge_action)

        if residual_battery_energy > 0:    
            if current_controlled_load_consumption > 0:
                residual_controlled_load_consumption = current_controlled_load_consumption - residual_battery_energy
            if current_general_electricity_consumption > 0:
                residual_general_electricity_consumption = current_general_electricity_consumption - residual_battery_energy

        cost = self.electricity_cost(residual_general_electricity_consumption, residual_controlled_load_consumption)
        reward = -cost
        done = True if self.datetime == datetime(2013, 12, 6, 23, 30) else False

        observations = [self.battery.battery_size, self.battery.current_charge, residual_general_electricity_consumption, residual_controlled_load_consumption]

        return observations, reward, done



    def electricity_cost(self, general_electricity_consumption, controlled_load_consumption):
        general_consumption_cost = self.single_rate_tariff * general_electricity_consumption
        controlled_consumption_cost = self.controlled_load_tariff * controlled_load_consumption

        step_cost = general_consumption_cost + controlled_consumption_cost
        return step_cost










