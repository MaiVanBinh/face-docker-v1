import datetime
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, Blueprint
from flask_restful import Api

from app.database.mongo import mongo
from app.config import config_of_flask

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def create_app():
    # path = os.path.abspath('static/') # default
    path = os.path.abspath('storage/app/public/')
    app = Flask(__name__, static_folder=path, static_url_path="")

    app.config.from_object(config_of_flask)
    # mongo.init_app(app) # not use flask-pymongo

    log_filename = os.path.join(app.config['LOG_PATH'], '{:%Y-%m-%d}.log'.format(datetime.date.today()))
    logging.basicConfig(filename=log_filename, level=logging.DEBUG,
                        format=f'%(asctime)s | %(levelname)s | %(name)s | %(threadName)s : %(message)s')

    logger = logging.getLogger(__name__)
    handler = logging.handlers.TimedRotatingFileHandler(log_filename, 'midnight', 1)
    handler.suffix = "%Y-%m-%d"
    logger.addHandler(handler)

    return app
