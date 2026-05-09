import pandas as pd

from iot_transform import filter_sensor_noise


def test_filter_sensor_noise():
    df = pd.DataFrame({"reading": [1.0, None, 3.0]})
    out = filter_sensor_noise(df)
    assert len(out) == 2
