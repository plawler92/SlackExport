import config
from pymongo import MongoClient
from pyslack import SlackClient

#this is used to initially load the channel data for the mongodb collection

mongo = MongoClient(config.mongo_string)
db = mongo.slack
mongo_channels = db.channels

existing_channels = []
for channel in mongo_channels.find():
    existing_channels.append(channel['channel_id'])

slack = SlackClient(config.token)

channels = slack.channel_listing('public_channel,private_channel')

mongo_docs = []

for channel in channels:
    if channel['id'] not in existing_channels:
        doc = {
            'channel_id': channel['id'],
            'channel_name': channel['name'],
            'is_private': channel['is_private']
        }

        mongo_docs.append(doc)

if mongo_docs:
    result = mongo_channels.insert_many(mongo_docs)
    print(result.inserted_ids)
