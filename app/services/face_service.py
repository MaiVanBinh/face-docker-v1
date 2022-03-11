import datetime
import os
import uuid as uuid_pkg

from flask import url_for

from api.application.get_faces_from_image import get_faces_from_image
from app import config_of_flask, constants
from app.database.mongo import mongo
from app.services import retrain_service, person_service
from app.utils import supporter
from app.utils.exceptions import LockWhenRetrainingError, PersonNotExistsError, MaxFaceRegisterError, UnknownError, \
    FaceNotExistsError, RegisterFaceError


def register_face(uuid, file):
    """
    Service - Register face
    :param uuid:
    :param file:
    :return:
    """
    last_retrain = retrain_service.get_last_retrain()  # will return False if empty retrain document
    if last_retrain:
        if last_retrain['status'] == constants.STATUS_RETRAIN_TRAINING:
            raise LockWhenRetrainingError

    filename_origin = file.filename
    person = person_service.get_by_uuid(uuid)

    if not person:
        raise PersonNotExistsError

    # check and limit face register - only 20 face
    max_face_register = config_of_flask.MAX_FACE_REGISTER
    face_current_count = 0
    if 'faces' in person:
        face_current_count = len(person['faces'])
    if face_current_count >= max_face_register:
        raise MaxFaceRegisterError(max_face_register)

    filename = supporter.convert_filename(file.filename)
    dirname = person['uuid']
    path_folder = supporter.make_folder_upload('persons', dirname)

    if not path_folder:
        raise UnknownError

    path_file_absolute = os.path.join(path_folder['full_path'], filename)
    file.save(path_file_absolute)

    public_path = os.path.join(path_folder['public_path'], filename)

    url_image = supporter.make_url(url_for('public_url', path=public_path))

    # get list filename trained from api/dataset/train and store to db
    images_face = get_faces_from_image(path_file_absolute, person['uuid'])

    if len(images_face) <= 0:
        supporter.remove_file_absolute_path(path_file_absolute)
        raise RegisterFaceError

    id_face = str(uuid_pkg.uuid4())
    create_face(uuid, {
        'image_path': public_path,
        'filename_origin': filename_origin,
        'id': id_face,
        'trains': images_face,
    })

    response = {
        'name': person['name'],
        'id': id_face,
        'filename': url_image,
    }

    return response


def delete_face(id):
    """
    Service - delete a face by id
    :param id:
    :return:
    """
    face = get_face_by_id(id)

    if face is None:
        raise FaceNotExistsError

    supporter.remove_face(face['faces'][0]['image_path'], face['uuid'], face['faces'][0]['trains'])

    delete_face_by_id(face['uuid'], id)

    response = {
        'person': {
            'name': face['name'],
            'uuid': face['uuid'],
        },
        'id': id
    }

    return response


def count_face():
    """
    Service - count all faces
    :return:
    """
    faces_count = count_all_faces()
    response = {
        'total': faces_count,
    }

    return response


# Functions support for service
def get_face_by_id(id):
    """
    Get face by face id
    :param id:
    :return:
    """
    person_model = mongo.persons

    query = {'faces.id': id}
    select = {'_id': 0, 'faces': {'$elemMatch': {'id': id}}, 'name': 1, 'uuid': 1}

    person = person_model.find_one(query, select)

    return person


def create_face(uuid, data):
    """
    Create face in person
    :param uuid:
    :param data:
    :return:
    """
    time = datetime.datetime.now()
    person = mongo.persons

    query = {'uuid': uuid}

    values = {
        "$push": {
            'faces': data
        },
        "$set": {
            'updated_at': time,
        }
    }

    person.update_one(query, values, upsert=True)


def delete_face_by_id(uuid, id):
    """
    Delete face by face id
    :param uuid:
    :param id:
    :return:
    """
    person_model = mongo.persons

    query = {'uuid': uuid}
    pull = {'$pull': {'faces': {'id': id}}}

    person_model.update(query, pull)

    return True


def count_all_faces():
    """
    Count all faces in system
    :return:
    """
    faces_count = 0

    person_model = mongo.persons

    result = person_model.aggregate([
        {'$match': {}},
        {'$unwind': "$faces"},
        {'$group': {'_id': None, 'count': {'$sum': 1}}},
    ])

    result = list(result)
    if len(result) > 0:
        result = result[0]
        if 'count' in result:
            faces_count = result['count']

    return faces_count
