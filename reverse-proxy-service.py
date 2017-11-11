from flask import Flask
from flask_cors import CORS
from flask import request
from flask import Response
import requests
from gevent.wsgi import WSGIServer # For better concurrent request handling
app = Flask(__name__)
CORS(app)
http_server = WSGIServer(('', 5000), app)

app = Flask(__name__)

url = 'http://webservices.nextbus.com/service/publicXMLFeed?'


@app.route('/api/v1/config', methods=['GET'])
def config():
    command = request.args.get('command')
    data = {}
    config_url = url + 'command=' + command
    if command == 'agencyList':
        resp = requests.get(config_url)
        response_time = resp.elapsed.total_seconds()
        data = Response(resp, status=200, mimetype='application/xml')
        print config_url, response_time
    elif command == 'routeList':
        agency_tag = request.args.get('a')
        config_url = config_url + '&a=' + agency_tag
        resp = requests.get(config_url)
        response_time = resp.elapsed.total_seconds()
        data = Response(resp, status=200, mimetype='application/xml')
        print config_url, response_time
    elif command == 'routeConfig':
        agency_tag = request.args.get('a')
        if request.args.get('r'):
            route = request.args.get('r')
            config_url = config_url + '&a=' + agency_tag + '&r=' + route
        else:
            config_url = config_url + '&a=' + agency_tag
        resp = requests.get(config_url)
        response_time = resp.elapsed.total_seconds()
        data = Response(resp, status=200, mimetype='application/xml')
        print config_url, response_time
    return data


@app.route('/api/v1/predictions', methods=['GET'])
def predictions():
    command = request.args.get('command')
    data = {}
    config_url = url + 'command=' + command
    if command == 'agencyList':
        resp = requests.get(config_url)
        response_time = resp.elapsed.total_seconds()
        data = Response(resp, status=200, mimetype='application/xml')
        print config_url, response_time
    elif command == 'routeList':
        agency_tag = request.args.get('a')
        config_url = config_url + '&a=' + agency_tag
        resp = requests.get(config_url)
        response_time = resp.elapsed.total_seconds()
        data = Response(resp, status=200, mimetype='application/xml')
        print config_url, response_time
    elif command == 'routeConfig':
        agency_tag = request.args.get('a')
        if request.args.get('r'):
            route = request.args.get('r')
            config_url = config_url + '&a=' + agency_tag + '&r=' + route
        else:
            config_url = config_url + '&a=' + agency_tag
        resp = requests.get(config_url)
        response_time = resp.elapsed.total_seconds()
        data = Response(resp, status=200, mimetype='application/xml')
        print config_url, response_time
    return data


if __name__ == '__main__':
    app.run()
