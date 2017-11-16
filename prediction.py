from flask import request, Response, Blueprint
from utils import BASE_URL, proxy_request, update_count_db

prediction_blueprint = Blueprint('prediction', __name__)


@prediction_blueprint.route('/api/v1/prediction', methods=['GET'])
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
    update_count_db(prediction_url, response_time)
    return data