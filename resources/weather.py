from flask import request, jsonify
from flask_restful import Resource, abort
from marshmallow import Schema, fields
from services.weather_service import WeatherService
from utils.constants import API_STATUS_OK, API_STATUS_NOT_OK


class WeatherSchema(Schema):
    """
    A class to represent the WeatherSchema

    ...

    Fields
    ------

    city: str, required
    country: str, required

    """
    city = fields.Str(required=True)
    country = fields.Str(required=True)


schema = WeatherSchema()


class Weather(Resource):
    """
    A class to represent the Weather (Resource)

    ...

    Methods
    -------
    get():
        Gets the latest post based on parameters number of posts.

    validate_post_maximum_length(self, post: dict) -> bool:
        Checks the maximum length of the post content

    validate_maximum_posts_per_day(self, username: str) -> bool:
        Checks the maximum posts per day of the user

    add_post(post: dict) -> str:
        Adds new posts to repositories.

    get_user_posts_count(username: str) -> int:
        Gets the total count of users posts.
    """

    @staticmethod
    def get():
        """
        The GET method requests representation of a specific resource.

        Parameters
        ----------
            n/a

        Returns
        ----------
        The data requested
        """

        errors = schema.validate(request.args)
        if errors:
            return abort(400, errors=errors)

        weather = WeatherService(city=request.args.get("city"), country=request.args.get("country"))
        result = weather.get_weather_info()

        response = jsonify(result)
        response.headers = {"content-type": "application/json"}
        if result.get("cod", API_STATUS_OK) == API_STATUS_OK:
            response.status_code = API_STATUS_OK
        else:
            response.status_code = API_STATUS_NOT_OK

        return response
