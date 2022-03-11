from enum import Enum


class STATUS_CODE(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502

class STATUS_FILE(Enum):
    LOCAL = 0
    NETWORK = 1
    UPLOAD = 2
    
# status of train model
STATUS_RETRAIN_TRAINING = 'training'
STATUS_RETRAIN_COMPLETE = 'complete'
STATUS_RETRAIN_FAILED = 'failed'

# status of recognize use train model
STATUS_RECOGNITION_USING = 'using'
STATUS_RECOGNITION_NOT_USE = 'not_use'
