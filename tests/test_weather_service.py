import pytest
from weather_service import describe_weather, daily_rows, get_forecast


def test_describe_weather_known():
    assert describe_weather(0) == ('Trời quang', '☀️')


def test_describe_weather_unknown():
    assert describe_weather(999)[0] == 'Không xác định'


def test_daily_rows():
    payload = {'daily': {
        'time': ['2026-11-17'], 'weather_code': [61],
        'temperature_2m_max': [31.2], 'temperature_2m_min': [24.6],
        'precipitation_probability_max': [70], 'precipitation_sum': [4.1],
    }}
    rows = daily_rows(payload)
    assert len(rows) == 1
    assert rows[0]['Ngày'] == '17/11/2026'
    assert rows[0]['Khả năng mưa (%)'] == 70


def test_mismatched_lengths():
    payload = {'daily': {
        'time': ['2026-11-17'], 'weather_code': [],
        'temperature_2m_max': [31], 'temperature_2m_min': [24],
        'precipitation_probability_max': [70], 'precipitation_sum': [4],
    }}
    with pytest.raises(ValueError):
        daily_rows(payload)


def test_day_range_validation():
    with pytest.raises(ValueError):
        get_forecast(10, 106, 17)
