import os

from flask_cors import CORS

from app import create_app
from flask_restful import Api
from app.routes import routes
from flask import make_response, jsonify, Blueprint, request, redirect, url_for
from app.constants import STATUS_CODE
from app.middlewares.authentication import authentication

app = create_app()
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api_bp = Blueprint('api_v1_auth', __name__, url_prefix='/v1/auth')

app.before_request_funcs = {
    # blueprint name: [list_of_functions]
    'api_v1_auth': [authentication]
}

api = Api(api_bp)

# setup routes
# route for api is protected by authentication middleware
routes.initialize_routes(api)
app.register_blueprint(api_bp)

# with multiple blueprint
# api_bp_2 = Blueprint('api2', __name__, url_prefix='/api/v2')
# api_2 = Api(api_bp_2)
# initialize_routes_2(api_2)
# app.register_blueprint(api_bp_2)


@app.route('/', methods=['GET'])
def home():
    return make_response(jsonify({
        'project': 'S-Face',
        'version': '1.0.0',
        'author': 'S3Lab',
        'description': 'Face recognition',
    }))


@app.route('/files/<path:path>', methods=['GET'])
def public_url(path):
    """
    Route for make link public files
    :param path:
    :return:
    """
    path_file = os.path.join(path)
    path_file = path_file.replace('\\', '/')
    return redirect(url_for('static', filename=path_file), code=301)


# get exception 500 for write log and return json - only env production
@app.errorhandler(500)
def exceptions(exception):
    app.logger.error(exception)
    body = jsonify({'result': 'fail', 'message': STATUS_CODE.INTERNAL_SERVER_ERROR.name})
    status_code = STATUS_CODE.INTERNAL_SERVER_ERROR.value

    return body, status_code


@app.errorhandler(404)
def exceptions(exception):
    app.logger.error(exception)
    body = jsonify({'result': 'fail', 'message': STATUS_CODE.NOT_FOUND.name})
    status_code = STATUS_CODE.NOT_FOUND.value

    return body, status_code


def run():
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['FLASK_DEBUG'],
            load_dotenv=True)


if __name__ == '__main__':
    run()
