from flask_restful import Resource, request

from app.services import face_service
from app.utils.restfuls import make_common_response
from app.utils import supporter
from app.utils.exceptions import PersonNotExistsError, UnknownError, LockWhenRetrainingError, MaxFaceRegisterError, \
    FaceNotExistsError, RegisterFaceError


class RegisterFace(Resource):
    def post(self, uuid):
        """
        Register face for person
        :return:
        """
        file = request.files['image']

        if not uuid:
            return make_common_response({}, 'Uuid is not empty.', True, status_code=400)

        if not file:
            return make_common_response({}, 'Image is not empty.', True, status_code=400)

        if not supporter.allowed_image(file.filename):
            return make_common_response({}, 'File type is not supported. Only support png, jpg, jpeg.', True,
                                        status_code=400)

        try:
            response = face_service.register_face(uuid, file)

            return make_common_response(response, "Register a face for person successfully.", status_code=200)
        except PersonNotExistsError:
            return make_common_response({}, 'Person does not exist.', True, status_code=400)
        except LockWhenRetrainingError:
            return make_common_response({},
                                        'The feature is locked because retraining the model. Please wait for the '
                                        'retrain to complete before you can retrain again.',
                                        True, status_code=200)
        except MaxFaceRegisterError as e:
            return make_common_response({}, 'Only up to ' + str(e.max) + ' faces can be registered.', True,
                                        status_code=400)
        except RegisterFaceError as e:
            return make_common_response({}, 'Face registration failed because no faces were detected.', True,
                                        status_code=400)
        except UnknownError:
            return make_common_response({}, 'An error occurred, please try again.', True, status_code=500)


class FaceDelete(Resource):
    def delete(self, id):
        if not id:
            return make_common_response({}, 'ID is not empty.', True, status_code=400)

        try:
            response = face_service.delete_face(id)

            return make_common_response(response, 'Delete registered face successfully.', status_code=200)
        except FaceNotExistsError:
            return make_common_response({}, 'Face not found.', True, status_code=400)


class FaceCount(Resource):
    def get(self):
        response = face_service.count_face()

        return make_common_response(response, status_code=200)
