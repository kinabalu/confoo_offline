import time 
import requests
import urllib
import json
from pymongo import MongoClient
from pymongo.errors import InvalidId
from bson import BSON
from bson import json_util
from bson.objectid import ObjectId
import scrapy

client = MongoClient('mongodb://boot2docker:27017')
db = client.confoo

def process_talks():
    json_data=open('talks.json')

    data = json.load(json_data)

    for entry in data:
        talk = db.talks.find_one({"url": entry['url'][0]})
        if talk is None:
            talk = dict()

        talk['title'] = entry['title'][0]
        talk['session_id'] = entry['id'][0]
        talk['url'] = entry['url'][0]
        talk['speaker_url'] = entry['speaker_url'][0]

        db.talks.save(talk)

    json_data.close()

    detail_data = open('talk_details.json')

    data = json.load(detail_data)
    for entry in data:
        talk = db.talks.find_one({"url": entry['url']})
        if talk is None:
            continue        # this ... is bad
        talk['description'] = entry['description'][0]
        room = entry['room']
        if len(room) > 0:
            talk['room'] = entry['room'][0]
        talk['date'] = entry['date'][0]
        talk['time'] = entry['time'][0]
        db.talks.save(talk)

    detail_data.close()

def process_speakers():
    json_data=open('speakers.json')

    data = json.load(json_data)

    for entry in data:
        speaker = db.speakers.find_one({"url": entry['url']}) 
        if speaker is None:
            speaker = dict() 

        speaker['url'] = entry['url']
        speaker['name'] = entry['name'][0]
        if len(entry['bio']) > 0:
            speaker['bio'] = entry['bio'][0] 
        speaker['speaker_photo'] = entry['speaker_photo'][0]
        if len(entry['company_url']) > 0:
            speaker['company_url'] = entry['company_url'][0]
        if len(entry['twitter']) > 0:
            speaker['twitter'] = entry['twitter'][0]

        oid = db.speakers.save(speaker)

        if 'talks' not in speaker:
            speaker['talks'] = []
            for talk_url in entry['talks']:
                talk = db.talks.find_one({"url": talk_url})
                if talk is None:
                    continue
                talk['_speaker_id'] = oid
                speaker['talks'].append(talk['_id'])
                db.talks.save(talk)
            db.speakers.save(speaker)

    json_data.close()

def main():
    process_talks()
    process_speakers()


if __name__ == '__main__':
    main()
