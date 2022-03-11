import datetime
import json
import logging
import os
import cv2
from pathlib import Path

from app.config import config_of_flask
from urllib.parse import unquote

ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg'}


def convert_filename(filename):
    """
    Create filename by time
    :param filename:
    :return:
    """
    file = filename.split('.')

    ext = file[-1]
    filename = str(int(datetime.datetime.now().timestamp())) + '.' + ext.lower()

    return filename


def make_folder_upload(parent, dirname=''):
    """
    Make folder upload for person if not exists
    :param parent: parent folder persons or recognizes
    :param dirname: sub-folder
    :return:
    """
    path = os.path.join(config_of_flask.PUBLIC_PATH, 'uploads', parent, dirname)
    try:
        Path(path).mkdir(parents=True, exist_ok=True)

        return {
            'full_path': path,
            'public_path': os.path.join('uploads', parent, dirname)
        }
    except Exception:
        logging.exception('Create folder failed:')

        return False


def allowed_image(filename):
    """
    Check allow image extension
    :param filename:
    :return:
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE


def remove_folder_upload_person(dirname):
    """
    Remove folder upload of person
    :param dirname:
    :return:
    """
    path = os.path.join(config_of_flask.PUBLIC_PATH, 'uploads', 'persons', dirname)

    try:
        if os.path.exists(path):
            for filename in os.listdir(path):
                os.remove(os.path.join(path, filename))
            os.rmdir(path)

        # remove folder train of uuid in datasets folder
        remove_train_folder(dirname)

        return True
    except OSError as error:
        logging.exception('Remove folder failed:')

        return False


def get_str_timestamp():
    """
    Get string timestamp
    :return:
    """
    return str(int(datetime.datetime.now().timestamp()))


def make_url(path):
    """
    Create link with domain from url
    :param path:
    :return:
    """
    if path[0] == '/':
        path = path.lstrip("/")
    last_char = config_of_flask.APP_URL[-1]
    if last_char == '/':
        url = unquote(config_of_flask.APP_URL + path)
    else:
        url = unquote(config_of_flask.APP_URL + '/' + path)

    return url.replace('\\', '/')


def remove_face(image_path, uuid, train_files):
    """
    Remove a face image
    :param image_path: path of image user upload
    :param uuid: uuid of person
    :param train_files: list file is gotten face from image upload
    :return:
    """
    path = os.path.join(config_of_flask.PUBLIC_PATH, image_path)

    try:
        if os.path.exists(path):
            os.remove(path)

        # remove file output in api/dataset/train
        for train_file in train_files:
            path_face_output = os.path.join(config_of_flask.DATASET_TRAIN_PATH, uuid, train_file)
            if os.path.exists(path_face_output):
                os.remove(path_face_output)

        return True
    except OSError:
        logging.exception('Remove a face image failed:')

        return False


def remove_train_folder(dirname):
    """
    Remove datasets/train folder
    :param: dirname:
    :return:
    """
    path = os.path.join(config_of_flask.DATASET_TRAIN_PATH, dirname)

    try:
        if os.path.exists(path):
            for filename in os.listdir(path):
                os.remove(os.path.join(path, filename))
            os.rmdir(path)

        return True
    except OSError as error:
        logging.exception('Remove folder failed:')

        return False


def get_image_size(file):
    """
    Get image size
    :param file: File image
    :return: (width, height)
    """
    img = cv2.imread(file)

    height, width, _ = img.shape
    del img

    return int(width), int(height)


def remove_old_model_folder(dirname):
    """
    Remove old model folder not use
    :return:
    """
    path = os.path.join(config_of_flask.ROOT_DIR, 'api', 'outputs', dirname)

    try:
        if os.path.exists(path):
            for filename in os.listdir(path):
                os.remove(os.path.join(path, filename))
            os.rmdir(path)

        return True
    except OSError as error:
        logging.exception('Remove folder failed:')

        return False


def remove_file_absolute_path(path):
    """
    Remove any file with absolute path
    :param path:
    :return:
    """
    if os.path.exists(path):
        os.remove(path)


def write_json_file(data, filepath):
    """
    write dât recognizes to image
    :param data:
    :param filepath:
    :return:
    """
    path = os.path.join(filepath, 'data.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def scale_image(image):
    """
    Scale image
    :param image:
    :return:
    """
    min_scale = 640
    img = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    h, w, _ = img.shape

    if h <= min_scale or w <= min_scale:
        return {
            'ratio': 1,
            'path_file': '',
        }

    if w > h:
        ratio = min_scale / w
    else:
        ratio = min_scale / h

    width = int(w * ratio)
    height = int(h * ratio)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    filename = os.path.basename(image) + '_' + str(int(datetime.datetime.now().timestamp())) + '_scaled.jpg'
    path = make_folder_upload('scales')
    path = os.path.join(path['full_path'], filename)
    cv2.imwrite(path, resized)
    del img
    del resized

    return {
        'ratio': ratio,
        'path_file': os.path.abspath(path),
    }


def draw_rectangle_face_detect(img_in, img_out, location):
    """
    Draw rectangle face detected
    :param img_in:
    :param img_out:
    :param location:
    :return:
    """
    img = cv2.imread(img_in)
    cv2.rectangle(img, (round(location[0]), round(location[1])), (round(location[2]), round(location[3])), (255, 0, 0), 2)

    cv2.imwrite(img_out, img)
    del img

def check_path(path):
    if not os.path.exists(path):
        return False

    if os.path.isdir(path):
        return 'DIR'
    elif os.path.isfile(path):
        return 'FILE'
