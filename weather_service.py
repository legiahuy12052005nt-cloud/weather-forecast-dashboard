"""Helpers for Open-Meteo weather forecasts."""
from __future__ import annotations

from datetime import datetime
import requests

FORECAST_URL = 'https://api.open-meteo.com/v1/forecast'
CITIES = {
    'TP. Hồ Chí Minh': (10.8231, 106.6297),
    'Hà Nội': (21.0285, 105.8542),
    'Đà Nẵng': (16.0544, 108.2022),
    'Huế': (16.4637, 107.5909),
    'Đà Lạt': (11.9404, 108.4583),
    'Cần Thơ': (10.0452, 105.7469),
    'Nha Trang': (12.2388, 109.1967),
    'Hải Phòng': (20.8449, 106.6881),
}

WEATHER_CODES = {
    0: ('Trời quang', '☀️'), 1: ('Chủ yếu nắng', '🌤️'),
    2: ('Có mây', '⛅'), 3: ('Nhiều mây', '☁️'),
    45: ('Có sương mù', '🌫️'), 48: ('Sương mù đóng băng', '🌫️'),
    51: ('Mưa phùn nhẹ', '🌦️'), 53: ('Mưa phùn', '🌦️'), 55: ('Mưa phùn dày', '🌧️'),
    56: ('Mưa phùn lạnh nhẹ', '🌧️'), 57: ('Mưa phùn lạnh', '🌧️'),
    61: ('Mưa nhẹ', '🌦️'), 63: ('Mưa vừa', '🌧️'), 65: ('Mưa lớn', '🌧️'),
    66: ('Mưa lạnh nhẹ', '🌧️'), 67: ('Mưa lạnh lớn', '🌧️'),
    71: ('Tuyết nhẹ', '🌨️'), 73: ('Tuyết vừa', '🌨️'), 75: ('Tuyết lớn', '❄️'),
    77: ('Hạt tuyết', '🌨️'), 80: ('Mưa rào nhẹ', '🌦️'),
    81: ('Mưa rào vừa', '🌧️'), 82: ('Mưa rào mạnh', '⛈️'),
    85: ('Tuyết rào nhẹ', '🌨️'), 86: ('Tuyết rào mạnh', '❄️'),
    95: ('Dông', '⛈️'), 96: ('Dông và mưa đá nhẹ', '⛈️'),
    99: ('Dông và mưa đá lớn', '⛈️'),
}


def describe_weather(code: int | None) -> tuple[str, str]:
    return WEATHER_CODES.get(code, ('Không xác định', '🌡️'))


def get_forecast(latitude: float, longitude: float, days: int = 7) -> dict:
    """Retrieve real-time/current and daily forecast data, raising on API errors."""
    if days < 1 or days > 16:
        raise ValueError('days phải nằm trong khoảng 1 đến 16')
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m',
        'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum',
        'timezone': 'auto',
        'forecast_days': days,
    }
    response = requests.get(FORECAST_URL, params=params, timeout=15)
    response.raise_for_status()
    result = response.json()
    if 'current' not in result or 'daily' not in result:
        raise ValueError('Phản hồi API thiếu dữ liệu thời tiết')
    return result


def daily_rows(payload: dict) -> list[dict]:
    """Convert parallel daily forecast arrays into one record per day."""
    daily = payload['daily']
    keys = ['time', 'weather_code', 'temperature_2m_max', 'temperature_2m_min',
            'precipitation_probability_max', 'precipitation_sum']
    if any(key not in daily for key in keys):
        raise ValueError('Dữ liệu dự báo theo ngày không đầy đủ')
    if len({len(daily[key]) for key in keys}) != 1:
        raise ValueError('Các cột dự báo không cùng số lượng ngày')
    rows = []
    for index, date in enumerate(daily['time']):
        label, symbol = describe_weather(daily['weather_code'][index])
        rows.append({
            'Ngày': datetime.fromisoformat(date).strftime('%d/%m/%Y'),
            'Tình trạng': f'{symbol} {label}',
            'Cao nhất (°C)': daily['temperature_2m_max'][index],
            'Thấp nhất (°C)': daily['temperature_2m_min'][index],
            'Khả năng mưa (%)': daily['precipitation_probability_max'][index],
            'Lượng mưa (mm)': daily['precipitation_sum'][index],
        })
    return rows
