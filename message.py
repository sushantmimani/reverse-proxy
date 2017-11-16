from flask import request, Response, Blueprint
from utils import BASE_URL, proxy_request, update_count_db

message_blueprint = Blueprint('message', __name__)


@message_blueprint.route('/api/v1/message', methods=['GET'])
def message():
    data = Response('Bad Request!Missing Parameters', status=400, mimetype='text')
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
        if route is None:
            return data
        time = request.args.get('t')
        if time is None:
            time = '0'
        message_url = message_url+'&r='+route+'&t='+time
        data, response_time = proxy_request(message_url)
    update_count_db(message_url, response_time)
    return data
