# gets weather from api
import requests
from config import *
weather_key = '2aeaafce-ce6e-4c02-bb92-62b9963fcaa8'


class WeatherAPI():
    def __init__(self):
        self.lat = '51.40480'
        self.lon = '39.13480'
        self.api_key = weather_key
        self.info = None
        self.weather = 'ясно'
        self.temp = '2 C'

    def get_weather_and_temp(self):
        request = f'https://api.weather.yandex.ru/v2/forecast?lat={self.lat}&lon={self.lon}'
        res = False# requests.get(request, headers={'X-Yandex-API-Key': self.api_key})
        if not(res):
            # print(res.status_code, res.reason)
            return 'ясно', '2 C'
        else:
            result = res.json()
            self.info = result
            temperature = result['fact']['temp']
            weather = result['fact']['condition']
            weather = weather_translate[weather]
            self.temp = temperature
            self.weather = weather
            return weather, str(temperature) + ' C'
