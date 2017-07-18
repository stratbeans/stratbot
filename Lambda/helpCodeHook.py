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
6
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

def help(intent_request):
    message = ""
    message += "To Assign a task to someone : *Assign <Work> to <Full Name on slack> by <Deadline>* or *Assign the task*\n"
    message += "To check your tasks or tasks id: *my tasks*\n"
    message += "To Mark the task complete: *task id <task_id> completed*\n"
    message += "To get details of a task: *show task id <id>*\n"
    message += "To check all open tasks : *open tasks* or *opentasks list*"
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': message})
    

def dispatch(intent_request):
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    return help(intent_request)

def lambda_handler(event, context):
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)   



