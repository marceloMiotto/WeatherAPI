"""
    Script to create the mongoDB database, collection and TTL index
"""

from pymongo import MongoClient
client = MongoClient()
db = client.weatherAPI
w = db.weather_db
w.create_index("inserted", expireAfterSeconds=120)


