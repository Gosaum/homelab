import flask

from api.routes import api_blueprint
from web.views import views_blueprint

def create_app():

    app = flask.Flask(__name__)
    app.register_blueprint(views_blueprint)
    app.register_blueprint(api_blueprint)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 