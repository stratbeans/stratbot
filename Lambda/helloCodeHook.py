import math
import dateutil.parser
import datetime
import time
import os
import logging
import urllib
import urllib2
import json
import boto3
import json

params = urllib.urlencode(dict({'token':'#'}))
req = urllib2.urlopen("https://slack.com/api/users.list?"+params)
ulist = json.loads(req.read())
uids = {}
unames = {}
if ulist['ok']:
    for m in ulist['members']:
        if m['profile']['real_name']:
            uids[m['profile']['real_name']] = m['id']
            unames[m['id']] = m['profile']['real_name']

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
    
def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response

def hello(intent_request):
    name = ''
    temp = intent_request['userId'].split(':')
    if len(temp)==3: 
        name = unames[temp[2]]
    else:
        name=''
    if name:
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Hey '+str(name)+", How can I help you?"})
    else:
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Hey, How can I help you?'})
        
def bye(intent_request):
    name = ''
    temp = intent_request['userId'].split(':')
    if len(temp)==3: 
        name = unames[temp[2]]
    else:
        name=''
    if name:
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Bye '+str(name)+"."})
    else:
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Bye'})

def dispatch(intent_request):
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name=="Hello":
        return hello(intent_request)
    elif intent_name=="GoodBye":
        return bye(intent_request)


def lambda_handler(event, context):
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)   



