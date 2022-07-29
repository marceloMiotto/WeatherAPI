from pymongo import MongoClient


def mongopy_conn():
    """
    Get the mongoDB connection, if not exists create it

    Parameters
    ----------
        N/A

    Returns
    ----------
    The repositories connection
    """

    client = MongoClient()
    db = client.weatherAPI
    return db


def weather_db():
    """
    Open the repositories connection

    Parameters
    ----------
        N/A

    Returns
    ----------
    The collection connection handler
    """
    try:
        db_conn = mongopy_conn()
    except ConnectionError as e:
        return f"Connection Error. {str(e)}"

    collection = db_conn.weather_db
    return collection

