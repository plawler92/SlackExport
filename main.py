import requests
import config
import json
from pymongo import MongoClient
from pyslack import SlackClient
from datetime import datetime

mongo = MongoClient(config.mongo_string)
db = mongo.slack
mongo_messages = db.messages

slack = SlackClient(config.token)

channels = slack.channel_listing('public_channel,private_channel')

mongo_docs = []

created_date = datetime.utcnow()
messagecount = 0
for channel in channels:
    messages = slack.message_listing(channel['id'])
    print(channel['name'] + ' ' + str(len(messages)))
    messagecount = messagecount + len(messages)
    for message in messages:
        doc = message
        ts = float(message['ts'])
        timestamp = int(ts)
        doc['channel'] = channel['name']
        doc['channelid'] = channel['id']
        doc['messagedate'] = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        doc['createddate'] = created_date
        del doc['ts']
        mongo_docs.append(doc)

print('expected: ' + str(messagecount))
print('actual: ' + str(len(mongo_docs)))
result = mongo_messages.insert_many(mongo_docs)
print(result)