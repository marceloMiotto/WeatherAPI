from datetime import datetime


class WeatherForecast:
    """
    A class to represent the Weather Forecast.

    ...

    Methods
    -------
    convert_fahrenheit_to_celsius() -> float:
        Converts the temperature from imperial to metrics

    add_forecast(forecast) -> None:
        Adds another WeatherForecast object to the forecast days

    timestamp_to_date(timestamp: datetime.timestamp) -> datetime:
        Converts from timestamp to datetime

    formatted_forecast(self):
        Gets the representation of a forecast on human-readable

    formatted_response(self) -> dict:
        Gets the representation of the response on human-readable
    """
    def __init__(self, city: str, country: str, temperature: float, wind_speed: str, wind_deg: str, cloudiness: str,
                 pressure: str, humidity: str, sunrise: int, sunset: int, lon: float, lat: float,
                 forecast_date: int):
        self.city = city
        self.country = country
        self.temperature_imperial = temperature
        self.temperature_metric = self.convert_fahrenheit_to_celsius()
        self.wind_speed = wind_speed
        self.wind_deg = wind_deg
        self.cloudiness = cloudiness
        self.pressure = pressure
        self.humidity = humidity
        self.sunrise = self.timestamp_to_date(sunrise).strftime("%H:%M:%S")
        self.sunset = self.timestamp_to_date(sunset).strftime("%H:%M:%S")
        self.lon = lon
        self.lat = lat
        self.requested_time = datetime.now()
        self.forecast = []
        self.forecast_date = self.timestamp_to_date(forecast_date).strftime("%b %d %Y %H:%M:%S")

    def convert_fahrenheit_to_celsius(self) -> float:
        """
        Converts the temperature from imperial to metrics.

        Parameters
        ----------
            n/a

        Returns
        ----------
        The converted temperature
        """

        return (self.temperature_imperial - 32) // 1.8

    def add_forecast(self, forecast) -> None:
        """
        Adds another WeatherForecast object to the forecast days.

        Parameters
        ----------
            forecast: WeatherForecast
                forecast is the same type of current forecast (daily)

        Returns
        ----------
            None
        """

        self.forecast.append(forecast)

    @staticmethod
    def timestamp_to_date(timestamp: datetime.timestamp) -> datetime:
        """
        Converts from timestamp to datetime

        Parameters
        ----------
            timestamp: datetime.timestamp

        Returns
        ----------
        The datetime from timestamp received as parameter
        """

        return datetime.fromtimestamp(timestamp)

    def formatted_forecast(self):
        """
        Gets the representation of a forecast on human-readable.

        Parameters
        ----------
            n/a

        Returns
        ----------
        The formatted weather forecast on human-readable
        """

        forecast_response = {"temperature": [f"{self.temperature_metric} C", f"{self.temperature_imperial} F"],
                             "wind": f"{self.wind_speed} m/s, {self.wind_deg}",
                             "cloudiness": f"{self.cloudiness} %",
                             "pressure": f"{self.pressure} hpa",
                             "humidity": f"self{self.humidity} %",
                             "sunrise": f"{self.sunrise}",
                             "sunset": f"{self.sunset}",
                             "date": self.forecast_date}

        return forecast_response

    def formatted_response(self) -> dict:
        """
        Gets the representation of the response on human-readable.

        Parameters
        ----------
            n/a

        Returns
        ----------
        The formatted response on human-readable
        """

        response = {"location_name": f"{self.city.capitalize()}, {self.country.upper()}",
                    "temperature": f"[{self.temperature_metric} C, {self.temperature_imperial} F]",
                    "wind": f"{self.wind_speed} m/s, {self.wind_deg}",
                    "cloudiness": f"{self.cloudiness} %",
                    "pressure": f"{self.pressure} hpa",
                    "humidity": f"self{self.humidity} %",
                    "sunrise": self.sunrise,
                    "sunset": self.sunset,
                    "geo_coordinates": f"[{self.lon}, {self.lat}]",
                    "requested_time": f"{self.requested_time:%Y-%m-%d %H:%M:%S}",
                    "forecast": [i.formatted_forecast() for i in self.forecast]}

        return response
