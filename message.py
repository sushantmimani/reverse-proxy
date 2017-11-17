"""
This module exposes an endpoint to proxy message commands to the
NextBus service

"""

from flask import request, Response, Blueprint
from utils import BASE_URL, proxy_request, update_count_db, extract_params

MESSAGE_BLUEPRINT = Blueprint('message', __name__)


@MESSAGE_BLUEPRINT.route('/api/v1/message', methods=['GET'])
def message():
    """
       This function checks the command received.
       Based on the command, it dynamically creates the URL and
       makes a request to the NextBus service

       """
    data = Response('Bad Request!Missing Parameters',
                    status=400,
                    mimetype='text')
    command, agency_tag = extract_params(request)
    #    If the params do not contain command and agency_tag an error is returned
    if not command or not agency_tag:
        return data
    message_url = BASE_URL + command + '&a=' + agency_tag
    if command == 'messages':
        # If no route is specified, get all messages
        if request.args.get('r'):
            routes = request.args.getlist('r')
            for route in routes:
                message_url = message_url+"&r="+route
        data, response_time = proxy_request(message_url)
    elif command == 'vehicleLocations':
        route = request.args.get('r')
        # If no route is specified, get vehicleLocations for all routes
        if route is not None:
            message_url = message_url + '&r=' + route
        time = request.args.get('t')
        if time is None:
            time = '0'
        message_url = message_url+'&t='+time
        data, response_time = proxy_request(message_url)
    update_count_db(message_url, response_time)
    return data
