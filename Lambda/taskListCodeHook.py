import math
import dateutil.parser
import datetime
import time
import os
import logging
import urllib2
#import ulrlib
import json
import boto3
import json
import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

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

def assign_task(intent_request):
    #payload = {'key1': 'value1', 'key2': 'value2'}
    #r = requests.post("http://httpbin.org/post", data=payload)
    #fromDate = get_slots(intent_request)['fromDate']
    #toDate = get_slots(intent_request)['toDate']
    source = intent_request['invocationSource']
    req = urllib2.urlopen("http://training.stratbeans.com/stratbot/opentasks")
    resp = json.loads(req.read())
    tasks = []
    print resp
    
    
    print intent_request['userId']
    if not resp['tasks']:
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': "No Open Tasks"})
    for task in resp['tasks']:
        tasks.append(str(task["task_id"])+" - "+str(task['user_name'])+" - "+str(task["details"])+"  by "+str(task['deadline']))
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': "\n".join(tasks)})
        
def dispatch(intent_request):
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    
    return assign_task(intent_request)



def lambda_handler(event, context):
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)   



