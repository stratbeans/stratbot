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

def assign_task(intent_request):
    print intent_request['userId']
    temp = intent_request['userId'].split(':')
    if len(temp)==3:
        uid = temp[2]
    else:
        return close(intent_request['sessionAttributes'],
                 'Failed',
                 {'contentType': 'PlainText',
                  'content': "Couldn't find your details" })
    source = intent_request['invocationSource']
    params = urllib.urlencode({'employee_id':uid})
    print uid
    req = urllib2.urlopen('http://training.stratbeans.com/stratbot/employeetask',params)
    resp = json.loads(req.read())
    if resp['ok']=='true':
        tasks = []
        print resp['tasks']
        if not resp['tasks']:
            return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': "No Open Tasks of yours."})
        for task in resp['tasks']:
            tasks.append("Task Id: "+str(task['task_id'])+'\n'+"Task Details: "+str(task['task_details'])+'\n'+'Deadline: '+str(task['deadline'])+'\n')
        tasks = "\n".join(tasks)
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': tasks})
    else:
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Some error occured. Kindly contact your Administratot'})
        
def dispatch(intent_request):
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    
    return assign_task(intent_request)



def lambda_handler(event, context):
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)   



