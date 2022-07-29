import os
from utils.constants import API_WEATHER_KEY, OPEN_WEATHER_URL, NUMBER_FORECAST_DAYS, API_STATUS_OK
from models.classes import WeatherForecast
from repositories.repository_weather_service import RepositoryWeatherService
import requests


class WeatherService(object):
    """
    A class to represent the WeatherService.

    ...

    Methods
    -------
    get_weather_api_key() -> str:
        Gets the OpenWeatherMap api key from environment variable (file .env)

    get_weather_current_day_url():
        Gets the formatted url for the day forecast

    get_weather_forecast_url():
        Gets the formatted url for the 10 days forecast

    get_weather_info_from_cache():
        Gets the forecast from cache (database)

    new_current_weather(response: dict) -> WeatherForecast:
        Creates a new WeatherForecast object to store the day forecast

    new_forecast(response: dict) -> WeatherForecast:
        Creates a new WeatherForecast object to store the daily forecast

    get_info_from_api() -> dict:
        Gets the weather forecast from OpenWeatherMap service

    save_to_cache(weather: dict) -> str:
        Saves the weather forecast into database

    get_weather_info(self):
        Handles the methods to retrieve the weather forecast. First tries to get from cache or from
        openweathermap otherwise
    """

    def __init__(self, city: str, country: str):
        self.city = city
        self.country = country
        self.forecast_list = []
        self.weather_db = RepositoryWeatherService(city=self.city, country=self.country)

    @staticmethod
    def get_weather_api_key() -> str:
        """
        Gets the OpenWeatherMap api key from environment variable (file .env)

        Parameters
        ----------
            n/a

        Returns
        ----------
        The api key from OpenWeatherMap from env file
        """
        return os.environ.get(API_WEATHER_KEY)

    def get_weather_current_day_url(self):
        """
        Gets the formatted url for the day forecast

        Parameters
        ----------
            n/a

        Returns
        ----------
        The formatted url for day forecast
        """
        return OPEN_WEATHER_URL + f"weather?q={self.city},{self.country}&units=imperial&appid=" + self.get_weather_api_key()

    def get_weather_forecast_url(self):
        """
        Gets the formatted url for the 10 days forecast

        Parameters
        ----------
            n/a

        Returns
        ----------
        The formatted url for daily forecast
        """
        return OPEN_WEATHER_URL + f"forecast/daily?q={self.city},{self.country}&units=imperial&cnt={NUMBER_FORECAST_DAYS}" \
                                  f"&appid=" + self.get_weather_api_key()

    def get_weather_info_from_cache(self):
        """
        Gets the forecast from cache (database)

        Parameters
        ----------
            n/a

        Returns
        ----------
        The weather forecast from database as a dict
        """
        return self.weather_db.get_weather_info()

    @staticmethod
    def new_current_weather(response: dict) -> WeatherForecast:
        """
        Creates a new WeatherForecast object to store the day forecast

        Parameters
        ----------
            response : dict
                the json representation of weather forecast from openweathermap service

        Returns
        ----------
        An object of type WeatherForecast
        """

        current_weather = WeatherForecast(city=response.get("name"),
                                          country=response.get("sys").get("country"),
                                          temperature=response.get("main").get("temp"),
                                          wind_speed=response.get("wind").get("speed"),
                                          wind_deg=response.get("wind").get("deg"),
                                          cloudiness=response.get("clouds").get("all"),
                                          pressure=response.get("main").get("pressure"),
                                          humidity=response.get("main").get("humidity"),
                                          sunrise=response.get("sys").get("sunrise"),
                                          sunset=response.get("sys").get("sunset"),
                                          lon=response.get("coord").get("lon"),
                                          lat=response.get("coord").get("lat"),
                                          forecast_date=response.get("dt"))

        return current_weather

    @staticmethod
    def new_forecast(response: dict) -> WeatherForecast:
        """
        Creates a new WeatherForecast object to store the daily forecast

        Parameters
        ----------
            response : dict
                the json representation of weather forecast from openweathermap service

        Returns
        ----------
        An object of type WeatherForecast to be aggregated to the response
        """

        weather_forecast = WeatherForecast(city="",
                                           country="",
                                           temperature=response.get("temp").get("day"),
                                           wind_speed=response.get("speed"),
                                           wind_deg=response.get("deg"),
                                           cloudiness=response.get("clouds"),
                                           pressure=response.get("pressure"),
                                           humidity=response.get("humidity"),
                                           sunrise=response.get("sunrise"),
                                           sunset=response.get("sunset"),
                                           lon=0,
                                           lat=0,
                                           forecast_date=response.get("dt"))

        return weather_forecast

    def get_info_from_api(self) -> dict:
        """
        Gets the weather forecast from OpenWeatherMap service

        Parameters
        ----------
            n/a

        Returns
        ----------
        The formatted response from the WeatherForecast object
        """

        # get the current day forecast
        response = requests.get(self.get_weather_current_day_url())
        if response.json().get("cod") == API_STATUS_OK:
            current_weather = self.new_current_weather(response.json())

            # get forecast days
            response = requests.get(self.get_weather_forecast_url())
            json_forecast = response.json()
            # print(json_forecast)
            for f in json_forecast.get("list"):
                forecast = self.new_forecast(f)
                current_weather.add_forecast(forecast)

            return current_weather.formatted_response()

        return response.json()

    def save_to_cache(self, weather: dict) -> str:
        """
        Saves the weather forecast into database

        Parameters
        ----------
            weather: dict
                the formatted response from WeatherForecast object to be saved as cache

        Returns
        ----------
        The id of the saved object from database
        """
        return self.weather_db.insert_weather_info(weather)

    def get_weather_info(self):
        """
        Handles the methods to retrieve the weather forecast. First tries to get from cache or from
        openweathermap otherwise

        Parameters
        ----------
            n/a

        Returns
        ----------
        The formatted response from the WeatherForecast object
        """
        # get the info from cache
        result = self.get_weather_info_from_cache()
        if result is None:
            result = self.get_info_from_api()
            if result.get("cod", API_STATUS_OK) == API_STATUS_OK:
                record_id = self.save_to_cache(result)
                del result["_id"]

        return result
