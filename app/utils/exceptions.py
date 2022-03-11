class CreatePersonError(Exception):
    """
    Create person error
    """
    pass


class PersonNotExistsError(Exception):
    """
    Person not exists error
    """
    pass


class LockWhenRetrainingError(Exception):
    """
    Feature is locked when retraining error
    """
    pass


class MaxFaceRegisterError(Exception):
    """
    Max face register error
    """

    def __init__(self, max):
        self.max = max

    pass


class UnknownError(Exception):
    """
    Unknown error
    """
    pass


class FaceNotExistsError(Exception):
    """
    Face not exists error
    """
    pass


class RecognizeError(Exception):
    """
    recognize error
    """
    pass


class RequiredRetrainModelError(Exception):
    """
    Required retrain model before recognize error
    """
    pass


class RegisterFaceError(Exception):
    """
    Register face error
    """
    pass


class TotalFaceTrainLess5Error(Exception):
    """
    Register face error
    """
    pass
