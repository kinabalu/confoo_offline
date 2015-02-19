from bottle import Bottle, run, request, response, abort
import json
import urllib
import requests
import pymongo
from pymongo import MongoClient

from pymongo.errors import InvalidId
from bson import BSON
from bson import json_util
from bson.objectid import ObjectId

app = Bottle()
client = MongoClient('mongodb://boot2docker:27017')
# client = MongoClient('mongodb://localhost:27017')
db = client.confoo


# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

@app.route('/api/talks', method='GET')
@enable_cors
def list_talks():
    talks = []

    filter = {}
    if 'filterBy' in request.query:
        filterBy = request.query['filterBy']
        if len(filterBy) > 0:
            filter = {"date": {"$in": [filterBy]}}

    # for talk in db.talks.find(filter).sort([("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)]):
    for talk in db.talks.find(filter):

        speaker = db.speakers.find_one({"_id": talk.get('_speaker_id')})
        talks.append({
            "id": str(talk.get("_id", "")),
            "title": talk.get('title', ""),
            "url": talk.get('url', ""),
            "time": talk.get('time', ""),
            "date": talk.get('date', ""),
            "room": talk.get('room', ""),
            "description": talk.get('description', ""),
            "speaker": {
                "name": speaker.get("name")
            }
        })

    result = dict()
    result['num_results'] = len(talks)
    result['total_pages'] = 1
    result['page'] = 1
    result['objects'] = talks

    response.content_type = 'application/json'    
    return json.dumps(result)

@app.route('/api/speakers', method='GET')
def list_speakers():
    speakers = []
    for speaker in db.speakers.find():
        speakers.append({
            "name": speaker.get('name', ""),
            "bio": speaker.get('bio', ""),
            "url": speaker.get('url', ""),
            "speaker_photo": speaker.get('speaker_photo', ""),
            "company_url": speaker.get('company_url', ""),
            "twitter": speaker.get('twitter', ""),
        })

    result = dict()
    result['num_results'] = len(speakers)
    result['total_pages'] = 1
    result['page'] = 1
    result['objects'] = speakers

    response.content_type = 'application/json'    
    return json.dumps(result)


@app.route('/api/talks/<talk_id>', method='GET')
@enable_cors
def get_talk(talk_id):
    response.content_type = 'application/json'    

    talk = db.talks.find_one({"_id": ObjectId(talk_id)})

    if talk is None:
        abort(404, 'Talk not found')

    speaker = db.speakers.find_one({"_id": talk.get('_speaker_id')})
    o_talk = {"id": str(talk.get("_id", "")),
        "title": talk.get('title', ""),
        "url": talk.get('url', ""),
        "time": talk.get('time', ""),
        "date": talk.get('date', ""),
        "room": talk.get('room', ""),
        "description": talk.get('description', ""),
        "speaker": {
            "name": speaker.get("name")
        }
    }
    return json.dumps(o_talk)


"""
@app.route('/stocks', method='POST')
def add_stock():
    try:
        postdata = request.body.read()
        symbol_request = json.loads(postdata)
        db.stocks.save({"symbol": symbol_request['symbol'], "price": 0.00})
    except TypeError:
        abort(500, "Invalid content passed")


@app.route("/talks", method="PUT")
@app.route("/talks", method="PATCH")
@app.route("/talks", method="DELETE")
def not_implemented():
  abort(405, "Method Not Allowed")


@app.route('/stocks/<symbol>', method='DELETE')
def delete_stock(symbol):
    response.content_type = 'application/json'

    ref_stock = db.stocks.find_one({"symbol": symbol})

    if ref_stock is None:
        abort(404)
        return

    db.stocks.remove({"symbol": symbol});
    return ''
"""

if __name__ == '__main__':
    # expand this out with args so we can swap between flup and not, and init the mongo with initial data
    # run(app, host='0.0.0.0', port=8282, server='flup')
    run(app, host='0.0.0.0', port=8080, debug=True)