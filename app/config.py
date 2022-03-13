import os
from dotenv import load_dotenv


class config_of_flask(object):
    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    LOG_PATH = os.path.join(ROOT_DIR, "storage", "logs")

    load_dotenv(verbose=True, dotenv_path=os.path.join(ROOT_DIR, ".env"))

    # app config
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 1)
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    HOST = os.getenv("FLASK_RUN_HOST", '0.0.0.0')
    PORT = os.getenv("FLASK_RUN_PORT", '5000')
    APP_URL = os.getenv("APP_URL")
    APP_NAME = os.getenv("APP_NAME", 'Face Recognition')

    MAX_FACE_REGISTER = int(os.getenv('MAX_FACE_REGISTER', 20))

    # config_path
    PUBLIC_PATH = os.path.join(ROOT_DIR, 'storage', 'app', 'public')
    DATASET_TRAIN_PATH = os.path.join(ROOT_DIR, 'api', 'datasets', 'train')


class config_db(object):
    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    load_dotenv(verbose=True, dotenv_path=os.path.join(ROOT_DIR, ".env"))

    DB_CONNECTION = 'mongodb'

    # mongo db config default
    MODE = os.getenv('MODE')
    if MODE == "Docker":
        MONGO_URI = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
    else:
        MONGO_URI = os.getenv('MONGO_URI')
    MONGO_HOST = os.getenv('MONGO_HOST')
    MONGO_PORT = os.getenv('MONGO_PORT')
    MONGO_USERNAME = os.getenv('MONGO_USERNAME')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
    MONGO_DATABASE = os.getenv('MONGO_DATABASE')

    if not MONGO_URI:
        if not MONGO_USERNAME:
            MONGO_URI = "mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}"
            MONGO_URI = MONGO_URI.format(MONGO_HOST=MONGO_HOST, MONGO_PORT=MONGO_PORT, MONGO_DATABASE=MONGO_DATABASE)
        else:
            MONGO_URI = "mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}"
            MONGO_URI = MONGO_URI.format(MONGO_HOST=MONGO_HOST, MONGO_PORT=MONGO_PORT, MONGO_PASSWORD=MONGO_PASSWORD,
                                         MONGO_USERNAME=MONGO_USERNAME, MONGO_DATABASE=MONGO_DATABASE)
    # end mongo default
