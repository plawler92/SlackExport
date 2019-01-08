import requests
import json

class SlackClient:

    def __init__(self, token):
        self.token = token
        self.api_url = 'https://slack.com/api/'
        self.conversations_list_method = 'conversations.list'
        self.conversations_history_method = 'conversations.history'

    #returns a list of dict's
    def channel_listing(self, types='public_channel,private_channel'):
        request_params = {
            'token': self.token,
            'types': types
        }

        r = requests.get(self.api_url + self.conversations_list_method, params=request_params)

        channels = []

        if r.status_code == 200:
            j = json.loads(r.text)
            channels = j['channels']
            
        return channels

    #returns a list of dict's
    def message_listing(self, channelid, *oldest):
        channel_messages = []
        request_string = self.api_url + self.conversations_history_method
        request_params = {
            'token': self.token,
            'channel': channelid
        }

        if oldest:
            request_params['oldest'] = oldest

        r = requests.get(request_string, params=request_params)
        
        j = json.loads(r.text)
        
        channel_messages.extend(j['messages'])

        while j['has_more'] == True:
            request_params['cursor'] = j['response_metadata']['next_cursor']
            r = requests.get(request_string, params = request_params)
            j = json.loads(r.text)
            channel_messages.extend(j['messages'])

        return channel_messages
    