import math


def parse_setpoint(text):
    """Parse '21.5C' or '70F' and return the temperature in Celsius.

    Returns None for any invalid input (None, empty, missing/unknown unit,
    non-numeric value, NaN/infinity).
    """
    if not isinstance(text, str):
        return None
    text = text.strip()
    if len(text) < 2:
        return None
    unit = text[-1].upper()
    if unit not in ("C", "F"):
        return None
    try:
        value = float(text[:-1])
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(value):
        return None
    if unit == "F":
        value = (value - 32) * 5 / 9
    if not math.isfinite(value):
        return None
    return round(value, 1)


def average_temperature(readings_csv):
    """Average a comma-separated list of readings.

    Returns None for None/empty input, empty elements, non-numeric or
    non-finite values, or an overflowing result.
    """
    if not isinstance(readings_csv, str) or not readings_csv.strip():
        return None
    values = []
    for item in readings_csv.split(","):
        try:
            number = float(item)
        except (ValueError, OverflowError):
            return None
        if not math.isfinite(number):
            return None
        values.append(number)
    average = sum(values) / len(values)
    if not math.isfinite(average):
        return None
    return average


def schedule_slot(time_text):
    """Label an 'HH:MM' time as 'night <min>' (before 06:00) or 'day <min>'.

    Returns None unless the text is exactly HH:MM with hour 0-23, minute 0-59.
    """
    if not isinstance(time_text, str):
        return None
    parts = time_text.strip().split(":")
    if len(parts) != 2:
        return None
    try:
        hour = int(parts[0])
        minute = int(parts[1])
    except ValueError:
        return None
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    if hour < 6:
        return "night " + str(minute)
    return "day " + str(minute)


def main():
    print("==== Running parse_setpoint ====")
    user_input = input("Enter a setpoint (e.g. 21.5C or 70F): ")
    result = parse_setpoint(user_input)
    print("Setpoint in Celsius:", result if result is not None else "Invalid input")

    print("\n==== Running average_temperature ====")
    user_input = input("Enter sensor readings as CSV (e.g. 20.5,21,22.5): ")
    result = average_temperature(user_input)
    print("Average Temperature:", result if result is not None else "Invalid input")

    print("\n==== Running schedule_slot ====")
    user_input = input("Enter a time as HH:MM (e.g. 07:30): ")
    result = schedule_slot(user_input)
    print("Schedule Slot:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()