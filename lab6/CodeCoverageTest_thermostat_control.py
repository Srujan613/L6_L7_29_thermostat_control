import pytest
from thermostat_control import target_temperature, hvac_action, energy_alert


# ---------- target_temperature ----------
def test_away_mode():
    assert target_temperature("away", True, 12) == 16

def test_sleep_night():
    assert target_temperature("sleep", True, 23) == 18

def test_unoccupied():
    assert target_temperature("home", False, 12) == 18

def test_morning_occupied():
    assert target_temperature("home", True, 7) == 22

def test_evening_occupied():
    assert target_temperature("home", True, 19) == 21

def test_default_occupied():
    assert target_temperature("home", True, 13) == 20


# ---------- hvac_action ----------
def test_idle():
    assert hvac_action(20, 20.5, 15) == "idle"

def test_heat_boost():
    assert hvac_action(15, 21, 0) == "heat_boost"

def test_heat():
    assert hvac_action(15, 21, 10) == "heat"

def test_cool_boost():
    assert hvac_action(28, 21, 35) == "cool_boost"


# ---------- energy_alert ----------
def test_no_readings():
    assert energy_alert([], 10) == "ok"

def test_critical():
    assert energy_alert([20, 30, 5], 10) == "critical"

def test_warning():
    assert energy_alert([20, 5, 5], 10) == "warning"
