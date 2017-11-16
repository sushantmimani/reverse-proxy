from flask import Flask
from flask_cors import CORS
from config import config_blueprint
from stats import stats_blueprint
from message import message_blueprint
from prediction import prediction_blueprint
from gevent.wsgi import WSGIServer  # For better concurrent request handling


app = Flask(__name__)
# Register all routes
app.register_blueprint(config_blueprint)
app.register_blueprint(stats_blueprint)
app.register_blueprint(message_blueprint)
app.register_blueprint(prediction_blueprint)
CORS(app)
http_server = WSGIServer(('0.0.0.0', 5000), app)


if __name__ == '__main__':
    http_server.serve_forever()
