"""
Util functions for the reverse-proxy service
"""

from pymongo import MongoClient
import requests
from bson.objectid import ObjectId
from flask import Response

BASE_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?command='
THRESHOLD = 0.5
CLIENT = MongoClient('db', 27017)
DB = CLIENT.reverseproxydb


def extract_params(req):
    """
    Function to keep track of proxy request and slow proxies
    """
    return req.args.get('command'), req.args.get('a')


def update_count_db(proxy_url, response_time):
    """
    Function to keep track of proxy request and slow proxies
    """
    item = DB.queries.find_one({"url": proxy_url})
    if item is None:
        DB.queries.insert_one({
            'url':proxy_url,
            'count':1
        })
    else:
        DB.queries.update_one({
            '_id':ObjectId(item['_id'])
        }, {
            '$set': {
                'count':item['count']+1
            }
        }, upsert=False)

    if response_time > THRESHOLD:
        DB.slow_requests.insert_one({
            'url': proxy_url,
            'time': response_time
        })


def proxy_request(config_url):
    """
    Function to make the API call to NextBus
    """
    resp = requests.get(config_url)
    response_time = resp.elapsed.total_seconds()
    data = Response(resp, status=200, mimetype='application/xml')
    return data, response_time
