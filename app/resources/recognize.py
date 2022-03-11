import os

from flask_restful import Resource, request

from app.services import recognize_service
from app.utils.exceptions import RecognizeError, RequiredRetrainModelError
from app.utils.restfuls import make_common_response
from app.utils.supporter import allowed_image, check_path
from urllib.parse import urlparse
import urllib
from app.constants import STATUS_FILE

class RecognizeImage(Resource):
    def post(self):
        """
        Recognize one image
        :return:
        """
        file = request.files["image"]

        if not file:
            return make_common_response(
                {}, "Image is not empty.", True, status_code=400
            )

        if not allowed_image(file.filename):
            return make_common_response(
                {},
                "File type is not supported. Only support png, jpg, jpeg.",
                True,
                status_code=400,
            )

        try:
            response = recognize_service.recognize_image(file)

            return make_common_response(
                response, "Recognize successfully.", status_code=200
            )
        except RecognizeError:
            return make_common_response({}, "Recognize failed.", True, status_code=200)
        except RequiredRetrainModelError:
            return make_common_response(
                {}, "Please retrain the model before recognize.", True, status_code=200
            )


class RecognizeImages(Resource):
    def post(self):
        """
        Recognize multiple images
        :return:
        """
        data = request.get_json()
        callback = ""
        path_folder = ""
        if "path" in data:
            path_folder = data["path"]
        else:
            return make_common_response({}, "Path is not empty.", True, status_code=400)

        if "callback" in data:
            callback = data["callback"]
        else:
            return make_common_response(
                {}, "Callback is not empty.", True, status_code=400
            )

        if not os.path.exists(path_folder):
            return make_common_response(
                {},
                "Path folder is empty or path folder not exists.",
                True,
                status_code=400,
            )

        try:
            response = recognize_service.recognize_images(path_folder, callback)

            return make_common_response(
                response, "Being recognize images in path.", status_code=200
            )
        except RequiredRetrainModelError:
            return make_common_response(
                {}, "Please retrain the model before recognize.", True, status_code=200
            )


class RecognizeImageByPath(Resource):
    def post(self):
        """
        Recognize multiple images by path
        :return:
        """
        data = request.get_json()
        callback = ""
        path_image = ""
        if data and "path" in data:
            path_image = data["path"]
        if not allowed_image(path_image):
            return make_common_response(
                {},
                "File type is not supported. Only support png, jpg, jpeg.",
                True,
                status_code=400,
            )
        pieces = urlparse(path_image)
        if pieces.scheme in ["http", "https", "ftp"]:
            response = "http"
            try:
                response = recognize_service.recognize_image(path_image, STATUS_FILE.NETWORK)
                return make_common_response(
                    response, "Being recognize images in path.", status_code=200
                )
            except RequiredRetrainModelError:
                return make_common_response(
                    {"image": "http"},
                    "Please retrain the model before recognize.",
                    True,
                    status_code=200,
                )
        elif check_path(path_image) == 'FILE':
            response = recognize_service.recognize_image(path_image, STATUS_FILE.LOCAL)
            return make_common_response(
                response,
                "Recognize successfully.",
                True,
                status_code=200,
            )
        else:
            return make_common_response(
                {},
                "Image file are not found",
                True,
                status_code=404,
            )
               
