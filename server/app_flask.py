from flask import Flask, jsonify, request, Response
from flask.ext.restful import Api, Resource, fields, marshal, abort
from flask.ext.restful.utils import cors

import json
import urllib
import requests
import pymongo
from pymongo import MongoClient

from pymongo.errors import InvalidId
from bson import BSON
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://boot2docker:27017')
# client = MongoClient('mongodb://localhost:27017')
db = client.confoo



class TalksAPI(Resource):

    def get(self):
        talks = []

        for talk in db.talks.find():

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

        return jsonify(result);
  

class TalksEntryAPI(Resource):

    def get(self, id):
        print id
        talk = db.talks.find_one({"_id": ObjectId(id)})

        print talk
        if talk is None:
            abort(404)

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
        return jsonify(o_talk)

class SpeakersAPI(Resource):

    def get(self):
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

        return jsonify(result)        

api.decorators = [cors.crossdomain(origin='*', headers=['accept', 'Content-Type', 'X-Requested-With'])]
api.add_resource(TalksAPI, '/api/talks', endpoint='talks')
api.add_resource(TalksEntryAPI, '/api/talks/<id>', endpoint='talks_entry')
api.add_resource(SpeakersAPI, '/api/speakers', endpoint='speakers')

if __name__ == '__main__':
    # expand this out with args so we can swap between flup and not, and init the mongo with initial data
    # run(app, host='0.0.0.0', port=8282, server='flup')
    app.run(host='0.0.0.0', port=8080, debug=True)