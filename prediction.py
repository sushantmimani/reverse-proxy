"""
This module exposes an endpoint to proxy prediction commands to the
NextBus service

"""

from flask import request, Response, Blueprint
from utils import BASE_URL, proxy_request, update_count_db, extract_params

PREDICTION_BLUEPRINT = Blueprint('prediction', __name__)


@PREDICTION_BLUEPRINT.route('/api/v1/prediction', methods=['GET'])
def prediction():
    """
        This function checks the command received.
        Based on the command, it dynamically creates the URL and
        makes a request to the NextBus service

        """
    data = Response('Bad Request!Missing parameters',
                    status=400,
                    mimetype='text')
    command, agency_tag = extract_params(request)
    # If request params do not contain a command or an agency, return an error
    if not command or not agency_tag:
        return data
    prediction_url = BASE_URL + command + '&a=' + agency_tag
    # Set useShortTitles flag based on the request params and update the request URL accordingly
    if request.args.get('useShortTitles'):
        use_short_titles = request.args.get('useShortTitles')
        prediction_url = prediction_url+'&useShortTitles=' + use_short_titles
    if command == 'predictions':
        # Predictions has 2 contracts. Form the required one based on the request params
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
            return data
        stops = request.args.getlist('stops')
        for stop in stops:
            prediction_url = prediction_url+"&stops="+stop
        data, response_time = proxy_request(prediction_url)
    elif command == 'schedule':
        route = request.args.get('r')
        if route is None:
            return data
        prediction_url = prediction_url+'&r='+route
        data, response_time = proxy_request(prediction_url)
    update_count_db(prediction_url, response_time)
    return data
