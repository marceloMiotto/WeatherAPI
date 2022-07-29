from unittest import TestCase
from models.classes import WeatherForecast


class TestWeatherForecast(TestCase):

    def setUp(self) -> None:
        self.wf = WeatherForecast(city="Porto Alegre", country="BR", temperature=32, wind_speed="5", wind_deg="5",
                                  cloudiness="10", pressure="2", humidity="98", sunrise=1545730073, sunset=1545730073,
                                  lon=15, lat=11, forecast_date=1545730073)

    def test_convert_fahrenheit_to_celsius(self):
        self.assertEqual(0, self.wf.convert_fahrenheit_to_celsius())

