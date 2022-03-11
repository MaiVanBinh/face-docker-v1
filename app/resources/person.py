import json

from flask_restful import Resource, request, reqparse
from app.services import person_service
from app.utils.exceptions import CreatePersonError, PersonNotExistsError
from app.utils.restfuls import make_common_response


class Persons(Resource):
    def get(self):
        """
        Get all person
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('filter', type=str, default='{}')
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)

        filter = json.loads(parser.parse_args().get('filter'))
        page = parser.parse_args().get('page')
        per_page = parser.parse_args().get('per_page')

        response = person_service.get_all_with_paginate(page, per_page, filter)

        return make_common_response(response, status_code=200)

    def post(self):
        """
        Create person
        :return:
        """
        data = request.get_json()
        if not data['name']:
            return make_common_response({}, 'Person name not is empty.', True, status_code=400)

        try:
            response = person_service.create_person(data)

            return make_common_response(response, 'Create person successfully.', status_code=201)
        except CreatePersonError:
            return make_common_response({}, 'Create person failed.', True, status_code=200)


class Person(Resource):
    def get(self, uuid):
        """
        Get person by uuid
        :return:
        """
        if not uuid:
            return make_common_response({}, 'Uuid is not empty.', True, status_code=400)

        try:
            response = person_service.get_person(uuid)

            return make_common_response(response, status_code=200)
        except PersonNotExistsError:
            return make_common_response({}, "Person not found.", True, 400)

    def delete(self, uuid):
        """
        Delete person
        :return:
        """
        if not uuid:
            return make_common_response({}, 'Uuid is not empty.', True, status_code=400)

        try:
            response = person_service.delete_person(uuid)

            return make_common_response(response, 'Delete person successfully.', status_code=200)
        except PersonNotExistsError:
            return make_common_response({}, 'Person does not exist.', True, status_code=400)

    def put(self, uuid):
        """
        Update person information
        :return:
        """
        if not uuid:
            return make_common_response({}, 'Uuid is not empty.', True, status_code=400)

        data = request.get_json()
        if not data['name']:
            return make_common_response({}, 'Person name not is empty.', True, status_code=400)

        try:
            response = person_service.update_person(uuid, data)

            return make_common_response(response, 'Update person successfully.', status_code=201)
        except Exception:
            return make_common_response({}, 'Update person failed.', True, status_code=500)
