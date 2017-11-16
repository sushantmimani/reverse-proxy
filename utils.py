from pymongo import MongoClient
import requests
from bson.objectid import ObjectId
from flask import Response

BASE_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?command='
THRESHOLD = 0.25


client = MongoClient(
    'db',
    27017)
db = client.reverseproxydb
'''
Function to keep track of proxy request and slow proxies
'''


def update_count_db(proxy_url, response_time):
    item = db.queries.find_one({"url":proxy_url})
    if item is None:
        db.queries.insert_one({
            'url':proxy_url,
            'count':1
        })
    else:
        db.queries.update_one({
            '_id':ObjectId(item['_id'])
        }, {
            '$set': {
                'count':item['count']+1
            }
        }, upsert=False)

    if response_time > THRESHOLD:
        db.slow_requests.insert_one({
            'url': proxy_url,
            'time': response_time
        })


'''
Function to make the API call to nextbus
'''


def proxy_request(config_url):
    resp = requests.get(config_url)
    response_time = resp.elapsed.total_seconds()
    data = Response(resp, status=200, mimetype='application/xml')
    return data, response_time

