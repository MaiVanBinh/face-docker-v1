import datetime
import uuid
import re

import pymongo
from flask import url_for

from app.database.mongo import mongo
from app.utils import supporter
from app.utils.exceptions import CreatePersonError, PersonNotExistsError
from app.utils.restfuls import paging_response


def create_person(data):
    """
    Service - Create person
    :param data:
    :return:
    """
    person_col = mongo.persons

    data_temp = data
    data_temp['uuid'] = str(uuid.uuid4())
    data_temp['created_at'] = datetime.datetime.now()
    data_temp['updated_at'] = datetime.datetime.now()

    person_id = person_col.insert(data_temp)

    query = {'_id': person_id}
    select = {'_id': 0}

    if person_col.count_documents(query, limit=1):
        person = person_col.find_one(query, select)

        response = {
            'name': person['name'],
            'uuid': person['uuid'],
        }

        return response

    raise CreatePersonError


def get_all_with_paginate(page, per_page, query=None):
    """
    Service - Get all person with paginate
    :param page:
    :param per_page:
    :param query:
    :return:
    """
    person_col = mongo.persons

    if query is None:
        query = {}

    select = {'_id': 0}
    skip = (page - 1) * per_page

    if 'name' in query:
        name_rgx = re.compile('.*' + str(query['name']) + '.*', re.IGNORECASE)  # compile the regex
        query['name'] = name_rgx

    persons = person_col.find(query, select).sort('created_at', pymongo.DESCENDING).skip(skip).limit(per_page)
    total = count_all_persons(query)

    result = []
    for person in persons:
        faces = []
        if 'faces' in person:
            for face in person['faces']:
                faces.append({
                    'id': face['id'],
                    'filename': supporter.make_url(url_for('public_url', path=face['image_path']))
                })

        result.append({
            'name': person['name'],
            'uuid': person['uuid'],
            'faces': faces,
        })

    response = {
        'list': result,
        'paging': paging_response(page, per_page, total)
    }

    return response


def get_person(uuid):
    """
    Service - Get one person by uuid
    :param uuid:
    :return:
    """
    person = get_by_uuid(uuid)

    if not person:
        raise PersonNotExistsError

    response = {
        'name': person['name'],
        'uuid': person['uuid'],
    }

    return response


def delete_person(uuid):
    """
    Service - Delete person by uuid
    :param uuid:
    :return:
    """
    person = get_by_uuid(uuid)
    if not person:
        raise PersonNotExistsError

    delete(uuid=uuid)

    response = {
        'name': person['name'],
        'uuid': person['uuid'],
    }

    # remove folder of person
    supporter.remove_folder_upload_person(dirname=uuid)

    return response


def update_person(uuid, data):
    """
    Service - update person information
    :return:
    """
    person = get_by_uuid(uuid)
    if not person:
        raise PersonNotExistsError

    update(uuid, data)

    response = {
        'name': data['name'],
        'uuid': person['uuid'],
    }

    return response


# Functions support for get data from database
def update(uuid, data):
    """
    update person with data
    :param id:
    :param data:
    :return:
    """
    person = mongo.persons

    query = {'uuid': uuid}

    data_temp = data
    data_temp['updated_at'] = datetime.datetime.now()

    values = {
        "$set": data_temp
    }

    person.update_one(query, values, upsert=True)


def get_all(query=None):
    """
    Get all persons information - query option
    :param query:
    :return:
    """
    person = mongo.persons

    if query is None:
        query = {}
    select = {'_id': 0}

    return list(person.find(query, select).sort('created_at', pymongo.DESCENDING))


def get_by_name(name):
    """
    Get person by name
    :param name:
    :return:
    """
    person = mongo.persons

    query = {'name': name}
    select = {'_id': 0}

    if person.count_documents(query, limit=1):
        return person.find_one(query, select)
    else:
        return False


def get_by_uuid(uuid):
    """
    Get person by uuid
    :param uuid:
    :return:
    """
    person = mongo.persons

    query = {'uuid': uuid}
    select = {'_id': 0}

    if person.count_documents(query, limit=1):
        return person.find_one(query, select)
    else:
        return False


def delete(name='', uuid=''):
    person = mongo.persons

    if name:
        query = {'name': name}
    else:
        query = {'uuid': uuid}

    person.delete_one(query)


def get_all_by_uuid(uuids):
    """
    Get all persons by list uuid
    :param uuids:
    :return:
    """
    person = mongo.persons

    query = {'uuid': {'$in': uuids}}
    select = {'_id': 0}

    return list(person.find(query, select))


def count_all_persons(query=None):
    """
    Count all persons
    :return: int
    """
    person_model = mongo.persons

    if query is None:
        query = {}

    return person_model.count_documents(query)
