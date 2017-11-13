from flask import Flask
from flask_cors import CORS
from flask import request
from flask import Response
import requests
import json
from gevent.wsgi import WSGIServer # For better concurrent request handling

app = Flask(__name__)
CORS(app)
http_server = WSGIServer(('0.0.0.0', 5000), app)


'''
Function to keep track of proxy request and slow proxies
'''


def update_count(proxy_url, response_time):
    if proxy_url not in proxy_count:
        proxy_count[proxy_url] = 1
    else:
        proxy_count[proxy_url] = proxy_count[proxy_url] + 1
    if response_time > THRESHOLD:
        slow_proxy[proxy_url] = response_time

'''
Function to make the API call to nextbus
'''


def proxy_request(config_url):
    resp = requests.get(config_url)
    response_time = resp.elapsed.total_seconds()
    data = Response(resp, status=200, mimetype='application/xml')
    return data, response_time


@app.route('/api/v1/stats', methods=['GET'])
def stats():
    resp = {
        'slow_requests': slow_proxy,
        'queries': proxy_count
    }
    return Response(json.dumps(resp), status=200, mimetype='application/json')


@app.route('/api/v1/config', methods=['GET'])
def config():
    data = Response('Bad Request! Missing parameters', status=400, mimetype='text')
    command = request.args.get('command')
    if not command:
        return data
    config_url = BASE_URL + command
    if command == 'agencyList':
        data, response_time = proxy_request(config_url)
    elif command == 'routeList' or command == 'routeConfig':
        agency_tag = request.args.get('a')
        if not agency_tag:
            return data
        else:
            config_url = config_url + '&a=' + agency_tag
        if command == 'routeList':
            data, response_time = proxy_request(config_url)
        elif command == 'routeConfig':
            if request.args.get('r'):
                route = request.args.get('r')
                config_url = config_url + '&a=' + agency_tag + '&r=' + route
            data, response_time = proxy_request(config_url)
    update_count(config_url, response_time)
    return data


@app.route('/api/v1/prediction', methods=['GET'])
def prediction():
    data = Response('Bad Request!', status=400, mimetype='text')
    command = request.args.get('command')
    agency_tag = request.args.get('a')
    if not command or not agency_tag:
        return data
    prediction_url = BASE_URL + command + '&a=' + agency_tag
    if request.args.get('useShortTitles'):
        use_short_titles = request.args.get('useShortTitles')
        prediction_url = prediction_url+'&useShortTitles=' + use_short_titles
    if command == 'predictions':
        if request.args.get('stopId'):
            stop_id = request.args.get('stopId')
            prediction_url = prediction_url + '&stopId=' + stop_id
            if request.args.get('r'):
                route = request.args.get('r')
                prediction_url = prediction_url + '&r=' + route
            data, response_time = proxy_request(prediction_url)
        elif request.args.get('s'):
            stop_tag = request.args.get('s')
            prediction_url = prediction_url + '&s=' + stop_tag
            if request.args.get('r'):
                route = request.args.get('r')
                prediction_url = prediction_url + '&r=' + route
            data, response_time = proxy_request(prediction_url)
    elif command == 'predictionsForMultiStops':
        if not request.args.get('stops'):
            return Response("Bad Request. Add at least 1 stop", status=400, mimetype='text')
        stops = request.args.getlist('stops')
        for stop in stops:
            prediction_url = prediction_url+"&stops="+stop
        data, response_time = proxy_request(prediction_url)
    elif command == 'schedule':
        route = request.args.get('r')
        prediction_url = prediction_url+'&r='+route
        data, response_time = proxy_request(prediction_url)
    update_count(prediction_url, response_time)
    return data


@app.route('/api/v1/message', methods=['GET'])
def message():
    data = Response('Bad Request!', status=400, mimetype='text')
    command = request.args.get('command')
    agency_tag = request.args.get('a')
    if not command or not agency_tag:
        return data
    message_url = BASE_URL + command + '&a=' + agency_tag
    if command == 'messages':
        if request.args.get('r'):
            routes = request.args.getlist('r')
            for route in routes:
                message_url = message_url+"&r="+route
        data, response_time = proxy_request(message_url)
    elif command == 'vehicleLocations':
        route = request.args.get('r')
        time = request.args.get('t')
        message_url = message_url+'&r='+route+'&t='+time
        data, response_time = proxy_request(message_url)
    update_count(message_url, response_time)
    return data


if __name__ == '__main__':
    BASE_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?command='
    THRESHOLD = 0.25
    proxy_count = {}
    slow_proxy = {}
    http_server.serve_forever()
