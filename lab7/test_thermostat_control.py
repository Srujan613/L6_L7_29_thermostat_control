import math
from hypothesis import given, strategies as st
from thermostat_control import parse_setpoint, average_temperature, schedule_slot


# ---------------- 1. "No crash" fuzz tests (random text and None) ----------------

@given(st.text() | st.none())
def test_parse_setpoint_no_crash(s):
    try:
        parse_setpoint(s)
    except Exception as e:
        assert False, f"parse_setpoint crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_average_temperature_no_crash(s):
    try:
        average_temperature(s)
    except Exception as e:
        assert False, f"average_temperature crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_schedule_slot_no_crash(s):
    try:
        schedule_slot(s)
    except Exception as e:
        assert False, f"schedule_slot crashed with: {e!r} for input {s!r}"


# ---------------- 2. Property tests (output must be sensible) ----------------

@given(st.text() | st.none())
def test_parse_setpoint_returns_none_or_finite_float(s):
    result = parse_setpoint(s)
    assert result is None or (isinstance(result, float) and math.isfinite(result))


@given(st.floats(min_value=-100, max_value=100, allow_nan=False),
       st.sampled_from(["C", "c", "F", "f"]))
def test_parse_setpoint_valid_inputs(value, unit):
    result = parse_setpoint(f"{value}{unit}")
    assert result is not None
    if unit.upper() == "C":
        assert result == round(value, 1)


@given(st.lists(st.floats(min_value=-100, max_value=100, allow_nan=False), min_size=1))
def test_average_is_between_min_and_max(values):
    result = average_temperature(",".join(str(v) for v in values))
    assert result is not None
    assert min(values) - 1e-6 <= result <= max(values) + 1e-6


@given(st.text() | st.none())
def test_average_returns_none_or_finite_float(s):
    result = average_temperature(s)
    assert result is None or (isinstance(result, float) and math.isfinite(result))


@given(st.integers(min_value=0, max_value=23), st.integers(min_value=0, max_value=59))
def test_schedule_slot_valid_times(hour, minute):
    result = schedule_slot(f"{hour:02d}:{minute:02d}")
    expected = ("night " if hour < 6 else "day ") + str(minute)
    assert result == expected


@given(st.text() | st.none())
def test_schedule_slot_returns_none_or_label(s):
    result = schedule_slot(s)
    assert result is None or result.startswith(("night ", "day "))