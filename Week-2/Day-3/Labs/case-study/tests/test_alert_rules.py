def alert_for_reading(temperature: float, moisture: float) -> str:
    """Mirrors `Labs/case-study/pipeline/main.py` alert ordering (temperature checked first)."""

    if temperature > 35:
        return "High Temp"
    if moisture < 40:
        return "Low Moisture"
    return "Normal"


def test_high_temperature_alert_wins_before_low_moisture():
    assert alert_for_reading(36, 10) == "High Temp"


def test_low_moisture_alert_when_temperature_not_high():
    assert alert_for_reading(30, 10) == "Low Moisture"


def test_normal_reading():
    assert alert_for_reading(30, 50) == "Normal"
