import pytest
from thermostat_control import target_temperature, hvac_action, energy_alert


# ---------- target_temperature ----------
def test_away_mode():
    assert target_temperature("away", True, 12) == 16

def test_sleep_early_morning():          # hour < 6 True
    assert target_temperature("sleep", True, 3) == 18

def test_sleep_late_night():             # hour < 6 False, hour >= 22 True
    assert target_temperature("sleep", True, 23) == 18

def test_sleep_daytime():                # both False
    assert target_temperature("sleep", True, 10) == 20

def test_sleep_boundaries():
    assert target_temperature("sleep", True, 6) == 20
    assert target_temperature("sleep", True, 22) == 18

def test_unoccupied():
    assert target_temperature("home", False, 12) == 18

def test_morning_occupied():
    assert target_temperature("home", True, 7) == 22

def test_morning_boundaries():
    assert target_temperature("home", True, 6) == 22
    assert target_temperature("home", True, 9) == 20

def test_evening_occupied():
    assert target_temperature("home", True, 19) == 21

def test_evening_boundaries():
    assert target_temperature("home", True, 17) == 21
    assert target_temperature("home", True, 22) == 20

def test_default_occupied():
    assert target_temperature("home", True, 13) == 20


# ---------- hvac_action ----------
def test_idle_small_positive_diff():
    assert hvac_action(20, 20.5, 15) == "idle"

def test_idle_small_negative_diff():
    assert hvac_action(20.5, 20, 15) == "idle"

def test_exactly_one_degree_not_idle():
    assert hvac_action(20, 21, 15) == "heat"

def test_heat_boost():
    assert hvac_action(15, 21, 0) == "heat_boost"

def test_heat_outside_boundary():
    assert hvac_action(15, 21, 5) == "heat"

def test_heat():
    assert hvac_action(15, 21, 10) == "heat"

def test_cool_boost():
    assert hvac_action(28, 21, 35) == "cool_boost"

def test_cool_outside_boundary():
    assert hvac_action(28, 21, 30) == "cool"

def test_cool():
    assert hvac_action(28, 21, 25) == "cool"


# ---------- energy_alert ----------
def test_no_readings():
    assert energy_alert([], 10) == "ok"

def test_all_within_limit():
    assert energy_alert([5, 10, 8], 10) == "ok"

def test_critical():
    assert energy_alert([20, 30, 5], 10) == "critical"

def test_warning():
    assert energy_alert([20, 5, 5], 10) == "warning"

def test_exactly_half_over_is_warning():
    assert energy_alert([20, 5], 10) == "warning"
