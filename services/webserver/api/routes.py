import flask

api_blueprint = flask.Blueprint('api', __name__, url_prefix='/api')

@api_blueprint.route('/ping', methods=['GET'])
def get_status():
    return {'status': 'ok'}, 200