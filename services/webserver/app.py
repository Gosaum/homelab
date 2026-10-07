import flask

from api.routes import api_blueprint
from api.sockets import monitor
from web.views import views_blueprint

def create_app(socketio):

    app = flask.Flask(__name__)
    app.register_blueprint(views_blueprint)
    app.register_blueprint(api_blueprint)

    socketio.init_app(app, async_mode="threading") # threading is the simplest option
    socketio.start_background_task(monitor, socketio)

    return app

from flask_socketio import SocketIO

socketio = SocketIO()
app = create_app(socketio)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)