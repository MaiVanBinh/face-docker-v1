from app.resources.hello import Hello
from app.resources.person import Person, Persons
from app.resources.face import RegisterFace, FaceDelete, FaceCount
from app.resources.retrain import RetrainModel, StatusModel, LastestModel, UpdateLatestModel
from app.resources.recognize import RecognizeImage, RecognizeImages, RecognizeImageByPath


def initialize_routes(api):
    api.add_resource(Hello, '/')

    api.add_resource(Persons, '/persons')  # GET, POST
    api.add_resource(Person, '/persons/<string:uuid>')  # GET, DELETE, PUT

    api.add_resource(RegisterFace, '/persons/<string:uuid>/face')  # POST
    api.add_resource(FaceDelete, '/faces/<string:id>')  # GET
    api.add_resource(FaceCount, '/faces/count')  # GET

    api.add_resource(RetrainModel, '/models/re-train')  # GET
    api.add_resource(StatusModel, '/models/status')  # GET
    api.add_resource(LastestModel, '/models/latest')  # GET
    api.add_resource(UpdateLatestModel, '/models/update-latest-model')  # GET
    
    api.add_resource(RecognizeImage, '/models/recognize')  # POST
    api.add_resource(RecognizeImages, '/models/recognizes')  # POST
    api.add_resource(RecognizeImageByPath, '/models/recognize-by-path')  # POST
