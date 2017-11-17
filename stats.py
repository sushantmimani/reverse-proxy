"""
This module exposes an endpoint to retrieve stats for the API requests
"""
import json
from flask import Response, Blueprint
from utils import DB

STATS_BLUEPRINT = Blueprint('stats', __name__)


@STATS_BLUEPRINT.route('/api/v1/stats', methods=['GET'])
def stats():
    """
    This function returns the API stats

    """
    queries = {}
    slow_requests = {}
    #  Retrieve items from MongoDB
    query_items = DB.queries.find()
    slow_queries = DB.slow_requests.find()
    # Create a dict from the data retrieved
    for item in query_items:
        queries[item['url']] = item['count']
    for item in slow_queries:
        slow_requests[item['url']] = item['time']
    resp = {
        'slow_requests': slow_requests,
        'queries': queries
    }
    return Response(json.dumps(resp), status=200, mimetype='application/json')
