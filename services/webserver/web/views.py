import flask

views_blueprint = flask.Blueprint('views', __name__)

@views_blueprint.route('/', methods=['GET'])
def index():
    return flask.render_template('home.html')