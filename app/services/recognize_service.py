import logging
import os
import threading
import requests
import shutil
import shutil

from flask import url_for

from api.application.recognizer_image import recognizer_image
from app import constants
from app.services import person_service, retrain_service
from app.utils.exceptions import RecognizeError, RequiredRetrainModelError
from app.utils.supporter import convert_filename, make_folder_upload, get_image_size, make_url, get_str_timestamp, \
    write_json_file, scale_image, draw_rectangle_face_detect
from werkzeug.utils import secure_filename
import urllib
from app.constants import STATUS_FILE

def recognize_image(file, statusFile=STATUS_FILE.UPLOAD):
    logging.info('Recognizing image...')
    if statusFile == STATUS_FILE.UPLOAD:
        filename = convert_filename(file.filename)
    elif statusFile == STATUS_FILE.LOCAL:
        # for path local image
        filename = file.split("\\")[-1]
    elif statusFile == STATUS_FILE.NETWORK:
        filename = file.split("/")[-1]
        
    path_folder = make_folder_upload('recognizes')
    path_file = os.path.join(path_folder['full_path'], filename)
    logging.info('Path: ' + path_file)
    if statusFile == STATUS_FILE.UPLOAD:
        file.save(path_file)
    elif statusFile == STATUS_FILE.LOCAL:
        if not os.path.isfile(filename):
            # copy file to folder recognizes
            shutil.copyfile(file, path_file)
    elif statusFile == STATUS_FILE.NETWORK:
        urllib.request.urlretrieve(file, path_file)
    # scale image if width or height bigger 640
    path_in_after_scale = path_file
    scale_ratio = 1
    # scale image
    scale_res = scale_image(path_file)
    if scale_res['ratio'] != 1:
        scale_ratio = scale_res['ratio']
        path_in_after_scale = scale_res['path_file']

    filename_output = filename.split('.')[0] + '_' + 'output.jpg'
    path_name_output = os.path.join(path_folder['full_path'], filename_output)

    # get last model complete information
    retrain_model = retrain_service.get_last_retrain({'status': constants.STATUS_RETRAIN_COMPLETE, 'removed_model': False})

    if not retrain_model:
        raise RequiredRetrainModelError

    if 'model_path' not in retrain_model:
        raise RequiredRetrainModelError

    model_folder = retrain_model['model_path']

    try:
        # update recognition_status for model is using
        retrain_service.update_retrain(retrain_model['id'], {'recognition_status': constants.STATUS_RECOGNITION_USING})

        # result = recognizer_image(pathImageIn=path_file, pathImageOut=path_name_output, model_folder=model_folder)
        result = recognizer_image(pathImageIn=path_in_after_scale, pathImageOut=path_name_output, model_folder=model_folder)
        retrain_service.update_retrain(retrain_model['id'], {'recognition_status': constants.STATUS_RECOGNITION_NOT_USE})
    except Exception:
        logging.exception('Recognize exception')
        retrain_service.update_retrain(retrain_model['id'], {'recognition_status': constants.STATUS_RECOGNITION_NOT_USE})
        raise RecognizeError

    # remove image was scaled
    if scale_res['ratio'] != 1:
        os.remove(path_in_after_scale)

    uuid_list = []
    data = {}
    data_unknowns = []
    for res in result:
        if res['name'] != 'Unknown':
            uuid_list.append(res["name"])
            data[res["name"]] = res
        else:
            data_unknowns.append(res)

    persons = person_service.get_all_by_uuid(uuid_list)

    width, height = get_image_size(path_file)
    public_path = os.path.join(path_folder['public_path'], filename)
    url_image = make_url(url_for('public_url', path=public_path))

    responses = []
    for person in persons:
        recognize_info = data[person['uuid']]
        location = [recognize_info['startPoint'][0] / scale_ratio, recognize_info['startPoint'][1] / scale_ratio,
                         recognize_info['endPoint'][0] / scale_ratio, recognize_info['endPoint'][1] / scale_ratio]
        responses.append({
            'name': person['name'],
            'uuid': person['uuid'],
            'location': location,
        })
        draw_rectangle_face_detect(os.path.join(path_folder['full_path'], filename),
                                   os.path.join(path_folder['full_path'], filename), location)

    for data_unknown in data_unknowns:
        location = [data_unknown['startPoint'][0] / scale_ratio, data_unknown['startPoint'][1] / scale_ratio,
                         data_unknown['endPoint'][0] / scale_ratio, data_unknown['endPoint'][1] / scale_ratio]
        responses.append({
            'name': data_unknown['name'],
            'location': location,
        })
        draw_rectangle_face_detect(os.path.join(path_folder['full_path'], filename),
                                   os.path.join(path_folder['full_path'], filename), location)

    response = {
        'file': url_image,
        'width': width,
        'height': height,
        'persons': responses,
    }

    return response


def recognize_images(path_folder, callback):
    """
    Service - recognize multiple image in path folder
    :return:
    """
    logging.info('Start recognize multiple images in folder path...')

    # get last model complete information
    retrain_model = retrain_service.get_last_retrain({'status': constants.STATUS_RETRAIN_COMPLETE, 'removed_model': False})

    if not retrain_model:
        raise RequiredRetrainModelError

    if 'model_path' not in retrain_model:
        raise RequiredRetrainModelError

    thread = threading.Thread(target=recognize_images_threading, args=(path_folder, callback, retrain_model,))
    thread.daemon = True
    thread.start()

    response = {}

    return response


def recognize_images_threading(path_folder, callback, retrain_model):
    """
    Recognize images threading
    :param retrain_model:
    :param path_folder:
    :param callback:
    :return:
    """
    files = os.listdir(path_folder)
    path_folder_output = make_folder_upload('recognizes')

    model_folder = retrain_model['model_path']
    data_all = []
    try:
        # update recognition_status for model is using
        retrain_service.update_retrain(retrain_model['id'], {'recognition_status': constants.STATUS_RECOGNITION_USING})

        for file in files:
            tmp_path_file = os.path.join(path_folder, file)

            if os.path.isfile(tmp_path_file) and (
                    file.find('.jpg') >= 0 or file.find('.jpeg') >= 0 or file.find('.png') >= 0):

                # scale image if width or height bigger 640
                path_in_after_scale = tmp_path_file
                scale_ratio = 1
                # scale image
                scale_res = scale_image(tmp_path_file)
                if scale_res['ratio'] != 1:
                    scale_ratio = scale_res['ratio']
                    path_in_after_scale = scale_res['path_file']

                filename_output = secure_filename(path_folder).lower() + '_' + get_str_timestamp() + '_output.jpg'
                path_name_output = os.path.join(path_folder_output['full_path'], filename_output)

                # result = recognizer_image(pathImageIn=tmp_path_file, pathImageOut=path_name_output, model_folder=model_folder)
                result = recognizer_image(pathImageIn=path_in_after_scale, pathImageOut=path_name_output, model_folder=model_folder)

                if scale_res['ratio'] != 1:
                    os.remove(path_in_after_scale)

                if result:
                    uuid_list = []
                    data = {}
                    data_unknowns = []
                    for res in result:
                        if res['name'] != 'Unknown':
                            uuid_list.append(res["name"])
                            data[res["name"]] = res
                        else:
                            data_unknowns.append(res)

                    persons = person_service.get_all_by_uuid(uuid_list)

                    width, height = get_image_size(tmp_path_file)

                    responses = []
                    for person in persons:
                        recognize_info = data[person['uuid']]
                        responses.append({
                            'name': person['name'],
                            'uuid': person['uuid'],
                            'location': [recognize_info['startPoint'][0] / scale_ratio, recognize_info['startPoint'][1] / scale_ratio,
                                         recognize_info['endPoint'][0] / scale_ratio, recognize_info['endPoint'][1] / scale_ratio],
                        })

                    for data_unknown in data_unknowns:
                        responses.append({
                            'name': data_unknown['name'],
                            'location': [data_unknown['startPoint'][0] / scale_ratio, data_unknown['startPoint'][1] / scale_ratio,
                                         data_unknown['endPoint'][0] / scale_ratio, data_unknown['endPoint'][1] / scale_ratio],
                        })

                    response = {
                        'file': tmp_path_file,
                        'width': width,
                        'height': height,
                        'persons': responses,
                    }

                    data_all.append(response)

        write_json_file(data_all, path_folder)
        retrain_service.update_retrain(retrain_model['id'], {'recognition_status': constants.STATUS_RECOGNITION_NOT_USE})
    except Exception:
        logging.exception('Recognize exception')
        retrain_service.update_retrain(retrain_model['id'], {'recognition_status': constants.STATUS_RECOGNITION_NOT_USE})

    if callback != '':
        response = requests.get(callback)
