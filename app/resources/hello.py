import os

from flask import make_response, jsonify
from flask_restful import Resource

from app.config import config_of_flask


class Hello(Resource):
    def get(self):
        return make_response(jsonify({'version_api': 'v1'}), 200)


class DocumentApi(Resource):
    def get(self):
        f = open(os.path.join(config_of_flask.ROOT_DIR, "document_api.json"), "r")

        return make_response(f.read(), 200)
