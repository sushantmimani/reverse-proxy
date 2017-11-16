from flask import request, Response, Blueprint
from utils import BASE_URL, proxy_request, update_count_db

config_blueprint = Blueprint('config', __name__)


@config_blueprint.route('/api/v1/config', methods=['GET'])
def config():
    data = Response('Bad Request! Missing parameters', status=400, mimetype='text')
    # Return an error if the request doesn't contain a command
    command = request.args.get('command')
    if not command:
        return data
    config_url = BASE_URL + command
    if command == 'agencyList':
        data, response_time = proxy_request(config_url)
    elif command == 'routeList' or command == 'routeConfig':
        # Return an error if the request command is routeList or routeConfig but there is no agency tag
        agency_tag = request.args.get('a')
        if not agency_tag:
            return data
        else:
            config_url = config_url + '&a=' + agency_tag
        if command == 'routeList':
            data, response_time = proxy_request(config_url)
        elif command == 'routeConfig':
            if request.args.get('r'):
                # If route is specified get the routeConfig for specified route, else all configs for the agency
                route = request.args.get('r')
                config_url = config_url + '&a=' + agency_tag + '&r=' + route
            data, response_time = proxy_request(config_url)
    # Update MongoDB to keep track of stats
    update_count_db(config_url, response_time)
    return data
