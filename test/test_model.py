from pytest import fixture

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
