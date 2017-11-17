"""
This is the driver file for the reverse proxy service
"""
from flask import Flask
from flask_cors import CORS
from gevent.wsgi import WSGIServer  # For better concurrent request handling
from config import CONFIG_BLUEPRINT
from stats import STATS_BLUEPRINT
from message import MESSAGE_BLUEPRINT
from prediction import PREDICTION_BLUEPRINT


APP = Flask(__name__)

APP.register_blueprint(CONFIG_BLUEPRINT)
APP.register_blueprint(STATS_BLUEPRINT)
APP.register_blueprint(MESSAGE_BLUEPRINT)
APP.register_blueprint(PREDICTION_BLUEPRINT)
CORS(APP)
HTTP_SERVER = WSGIServer(('0.0.0.0', 5000), APP)


if __name__ == '__main__':
    HTTP_SERVER.serve_forever()
