import math
import dateutil.parser
import datetime
import time
import os
import logging
import urllib2
import urllib
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
    taskid = get_slots(intent_request)['taskID']
    temp = intent_request['userId']
    temp = temp.split(':')
    uid = ''
    if len(temp)==3:
        uid = temp[2]
    payload = urllib.urlencode({'task_id': taskid,'user_id':uid })
    source = intent_request['invocationSource']
    req = urllib2.urlopen("http://training.stratbeans.com/stratbot/complete",payload)
    resp = json.loads(req.read())
    if resp['ok'] == 'true':
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Task with task id : {0} marked completed'.format(taskid)}
        )
    elif resp['ok'] == 'false':
        if resp['alreadyClosed']=='true':
            return close(intent_request['sessionAttributes'],
                     'Fulfilled',
                     {'contentType': 'PlainText',
                      'content': 'Task with task id {0} is already closed'.format(taskid)}
            )
        elif resp['wrongUser']=='true':
            return close(intent_request['sessionAttributes'],
                     'Fulfilled',
                     {'contentType': 'PlainText',
                      'content': 'Task with task id {0} does not belongs to you'.format(taskid)}
            )
        else:
            return close(intent_request['sessionAttributes'],
                     'Fulfilled',
                     {'contentType': 'PlainText',
                      'content': 'Task with task id {0} does not exist'.format(taskid)}
            )
def dispatch(intent_request):
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    
    return assign_task(intent_request)



def lambda_handler(event, context):
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)   



