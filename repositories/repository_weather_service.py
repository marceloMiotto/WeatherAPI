from repositories.mongodb import weather_db
import datetime


class RepositoryWeatherService(object):
    """
    A class to represent the Database Weather Service
    This tier is used as a cache
    ...

    Methods
    -------
    get_weather_info() -> dict:
        Gets the weather forecast info from cache for city and country

    insert_weather_info(weather: dict) -> str:
        Save the weather forecast info to be used as a cache

    """

    def __init__(self, city: str, country: str):
        self.city = city
        self.country = country

    def get_weather_info(self) -> dict:
        """
        Gets the weather forecast info from cache for city and country.

        Parameters
        ----------
            N/A

        Returns
        ----------
        The weather forecast info
        """

        col = weather_db()
        if col is str:
            return col
        return col.find_one({"location_name": f"{self.city.capitalize()}, {self.country.upper()}"}, {"_id": 0})

    @staticmethod
    def insert_weather_info(weather: dict) -> str:
        """
        Save the weather forecast info to be used as a cache.

        Parameters
        ----------
            weather : dict
                weather forecast info container

        Returns
        ----------
        The record object id from repositories

        """
        col = weather_db()
        weather["inserted"] = datetime.datetime.utcnow()
        record_id = str(col.insert_one(weather).inserted_id)
        return record_id
