import datetime
import logging
import os
import threading
import time
import uuid
from pathlib import Path

import pymongo

from app.config import config_of_flask
from api.application.train_softmax import train
from app import constants
from app.database.mongo import mongo
from app.services import person_service, face_service
from app.utils import supporter
from app.utils.exceptions import LockWhenRetrainingError, TotalFaceTrainLess5Error
from api.application.recognizer_image import reloadModel

def retrain_model():
    """
    Service - retrain the model
    :return:
    """
    logging.info('Start retrain the model...')
    # check and lock retrain when retraining
    last_retrain = get_last_retrain()  # will return False if empty retrain document
    if last_retrain:
        if last_retrain['status'] == constants.STATUS_RETRAIN_TRAINING:
            raise LockWhenRetrainingError

    count_all_faces = face_service.count_all_faces()
    if count_all_faces < 5:
        raise TotalFaceTrainLess5Error

    model_path = str(uuid.uuid4())
    path = os.path.join(config_of_flask.ROOT_DIR, 'api', 'outputs', model_path)
    Path(path).mkdir(parents=True, exist_ok=True)

    retrain = create_retrain(model_path)

    thread = threading.Thread(target=retrain_model_threading, args=(retrain,))
    thread.daemon = True
    thread.start()

    response = {
        'id': retrain['id'],
        'status': retrain['status'],
    }

    return response


def get_status_model():
    """
    Service - get status when retrain model
    :return:
    """
    retrain = get_last_retrain()
    
    persons = 0
    if not retrain:
        return {
            'id': '0',
            'status': constants.STATUS_RETRAIN_COMPLETE,
            'persons': persons
        }
    
    if 'persons' in retrain:
        persons = retrain['persons']

    response = {
        'id': retrain['id'],
        'status': retrain['status'],
        'persons': persons,
    }

    return response


def get_latest_model_current_use():
    """
    Service - Get last model current using
    :return:
    """
    query = {
        'status': constants.STATUS_RETRAIN_COMPLETE,
        'removed_model': False,
    }

    retrain = get_last_retrain(query)

    persons = 0
    if not retrain:
        return {
            'id': '0',
            'status': constants.STATUS_RETRAIN_COMPLETE,
            'persons': persons,
        }

    if 'persons' in retrain:
        persons = retrain['persons']

    updated_at = retrain['updated_at'].strftime("%Y-%m-%dT%H:%M:%SZ")
    response = {
        'id': retrain['id'],
        'status': retrain['status'],
        'persons': persons,
        'time': updated_at,
    }

    return response


def retrain_model_threading(retrain):
    """
    Threading retrain the model
    :param retrain: document of retrain
    :return:
    """
    try:
        status_train = train(retrain['model_path'])
        logging.info(status_train)

        update_retrain(retrain['id'], {'status': constants.STATUS_RETRAIN_COMPLETE}, True)
        logging.info('Finished retrain the model...')

        logging.info('Removing old the model folder not use...')
        # remove old model in api/outputs with recognition_status is not_use after retrain complete
        retrains_old = get_old_retrains(retrain['id'])
        logging.info(retrains_old)
        if len(retrains_old) > 0:
            for retrain_old in retrains_old:
                if 'model_path' in retrain_old:
                    # remove old model folder
                    supporter.remove_old_model_folder(retrain_old['model_path'])

                    # update model is removed
                    update_retrain(retrain_old['id'], {'removed_model': True})

        logging.info('Removed old the model folder successfully...')
    except Exception as e:
        logging.exception('Retrain model failed:')

        update_retrain(retrain['id'], {'data': constants.STATUS_RETRAIN_FAILED}, True)


def create_retrain(model_path):
    """
    Create retrain doc when retrain start
    :return:
    """
    retrain_col = mongo.retrains
    date_now = datetime.datetime.now()

    persons_count = person_service.count_all_persons()

    data_temp = {
        'id': str(uuid.uuid4()),
        'status': constants.STATUS_RETRAIN_TRAINING,
        'model_path': model_path,
        'recognition_status': constants.STATUS_RECOGNITION_NOT_USE,
        'removed_model': False,
        'persons': persons_count,
        'created_at': date_now,
        'updated_at': date_now,
    }

    retrain_id = retrain_col.insert(data_temp)

    query = {'_id': retrain_id}
    select = {'_id': 0}

    if retrain_col.count_documents(query, limit=1):
        return retrain_col.find_one(query, select)

    return False


def update_retrain(id, data, change_updated_at=False):
    """
    Update status retrain
    :param change_updated_at:
    :param id:
    :param data:
    :return:
    """
    retrain_col = mongo.retrains

    query = {'id': id}

    data_temp = data
    if change_updated_at:
        data_temp['updated_at'] = datetime.datetime.now()

    values = {
        "$set": data_temp
    }

    retrain_col.update_one(query, values, upsert=True)


def get_last_retrain(query=None):
    """
    Get last status retrain
    :param: query - filter query
    :return:
    """
    if query is None:
        query = {}

    retrain_col = mongo.retrains

    select = {'_id': 0}

    retrains = list(retrain_col.find(query, select).sort('updated_at', pymongo.DESCENDING).limit(1))
    if len(retrains) > 0:
        return retrains[0]

    return False


def get_old_retrains(id_ignore):
    """
    Get old retrains can remove model folder
    :param id_ignore: str
    :return:
    """
    retrain_col = mongo.retrains
    select = {'_id': 0}
    query = {
        'recognition_status': constants.STATUS_RECOGNITION_NOT_USE,
        'id': {'$ne': id_ignore},
        'removed_model': False,
    }

    retrains = list(retrain_col.find(query, select).sort('updated_at', pymongo.DESCENDING))

    return retrains

def update_latest_model():
    """
    Update latest models
    """
    reloadModel()