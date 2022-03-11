from flask_pymongo import PyMongo, MongoClient
from pymongo import uri_parser

from app.config import config_db


# mongo = PyMongo() # not use flask-pymongo

# db default
parsed_uri = uri_parser.parse_uri(config_db.MONGO_URI)
database_name = parsed_uri["database"]

client = MongoClient(config_db.MONGO_URI)
mongo = client[database_name]
