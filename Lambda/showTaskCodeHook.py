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
    taskid = get_slots(intent_request)['taskId']
    payload = urllib.urlencode({'task_id': taskid})
    source = intent_request['invocationSource']
    req = urllib2.urlopen("http://training.stratbeans.com/stratbot/showtask",payload)
    #print req.read()
    resp = json.loads(req.read())
    if resp['ok'] == 'true':
        message = "Task Details : "+resp['details']['task_details']+'\n'
        message += "Assigned To : "+resp['details']['user']+'\n'
        message += "Deadline : "+resp['details']['deadline']+'\n'
        message += 'Status : ' +resp['details']['status']+'\n'
        message += 'Assigned by : '+resp['details']['manager']+'\n'
        message += 'Created at :'+resp['details']['created_at']['date']
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': message }
        )
    elif resp['ok'] == 'false':
        return close(intent_request['sessionAttributes'],
                     'Fulfilled',
                     {'contentType': 'PlainText',
                      'content': 'Invalid task Id'.format(taskid)}
            )
def dispatch(intent_request):
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    
    return assign_task(intent_request)



def lambda_handler(event, context):
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)   



