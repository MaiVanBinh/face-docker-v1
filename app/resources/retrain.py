from flask_restful import Resource

from app import constants
from app.utils.exceptions import LockWhenRetrainingError, TotalFaceTrainLess5Error
from app.utils.restfuls import make_common_response
from app.services import retrain_service


class RetrainModel(Resource):
    def get(self):
        """
        Retrain model
        :return:
        """
        try:
            response = retrain_service.retrain_model()

            return make_common_response(response, 'Retraining the model. Please wait for retrain to complete.',
                                        status_code=200)
        except LockWhenRetrainingError:
            return make_common_response({},
                                        'The feature is locked because retraining the model. Please wait for the '
                                        'retrain to complete before you can retrain again.',
                                        True, status_code=200)
        except TotalFaceTrainLess5Error:
            return make_common_response({},
                                        'The total number of faces is less than 5, please register more faces for '
                                        'persons to train',
                                        True, status_code=200)


class StatusModel(Resource):
    def get(self):
        response = retrain_service.get_status_model()

        if response['id'] == '0':
            return make_common_response(response, 'Model does not exists. Please retrain the model.', status_code=200)

        if response['status'] == constants.STATUS_RETRAIN_TRAINING:
            return make_common_response(response, 'Retraining the model. Please wait for retrain to complete.',
                                        status_code=200)

        if response['status'] == constants.STATUS_RETRAIN_COMPLETE:
            return make_common_response(response, 'Retrain the model successfully.', status_code=200)

        if response['status'] == constants.STATUS_RETRAIN_FAILED:
            return make_common_response(response, 'Retrain the model failed.', status_code=200)


class LastestModel(Resource):
    def get(self):
        response = retrain_service.get_latest_model_current_use()

        if response['id'] == '0':
            return make_common_response(response, 'Model does not exists. Please retrain the model.', status_code=200)

        return make_common_response(response, status_code=200)

class UpdateLatestModel(Resource):
    def put(self):
        try:
            retrain_service.update_latest_model()
            return make_common_response({}, 'Update lated model success.', status_code=200)
        except:
            return make_common_response({}, 'Update lated model failed.', status_code=400)