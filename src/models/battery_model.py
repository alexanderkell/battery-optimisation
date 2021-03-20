from datetime import datetime, timedelta

class Battery:

    def __init__(battery_size=5000):
        self.battery_size = battery_size
        self.current_charge = 0


    def charge(charge_size):
        if self.current_charge + charge_size < self.battery_size:
            self.current_charge += charge_size
            return 0
        else:
            residual_energy = self.battery_size - self.current_charge
            self.current_charge = self.battery_size
            return residual_energy
            

    def discharge(discharge_size):
        if self.current_charge >= discharge_size:
            self.current_charge -= discharge_size
            return True
        else:
            return False

    def is_battery_full():
        if self.current_charge == self.battery_size:
            return True
        else:
            return False


class HouseSystem:

    time_step = timedelta(minutes=30)

    def __init__(battery_size, customer_number, generator_capacity, postcode, solar_generation, controlled_load_consumption, general_electricity_consumption):
        self.battery_size = battery_size
        self.battery = Battery(battery_size)
        self.customer_number = customer_number
        self.generator_capacity = generator_capacity
        self.postcode = postcode
        self.solar_generation = solar_generation
        self.controlled_load_consumption = controlled_load_consumption
        self.general_electricity_consumption
        self.datetime = datetime(2012, 1, 8, 0, 30)
    
    def step():
        self.datetime += time_step
        current_solar = self.solar_generation[self.solar_generation.datetime == self.datetime]
        current_controlled_load_consumption = self.controlled_load_consumption[self.controlled_load_consumption.datetime == self.datetime]
        current_general_electricity_consumption = self.general_electricity_consumption[self.general_electricity_consumption.datetime == self.datetime]

        if current_solar > 0 and self.battery.is_battery_full() is False:
            self.battery.charge(current_solar)




        




