from flask import Response, Blueprint
from pymongo import MongoClient
import json


stats_blueprint = Blueprint('stats', __name__)

client = MongoClient(
    'db',
    27017)
db = client.reverseproxydb


@stats_blueprint.route('/api/v1/stats', methods=['GET'])
def stats():
    queries = {}
    slow_requests = {}
    query_items = db.queries.find()
    slow_queries = db.slow_requests.find()
    for item in query_items:
        queries[item['url']] = item['count']
    for item in slow_queries:
        slow_requests[item['url']] = item['time']
    resp = {
        'slow_requests': slow_requests,
        'queries': queries
    }
    return Response(json.dumps(resp), status=200, mimetype='application/json')
