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

params = urllib.urlencode(dict({'token':'..'}))
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
    name = get_slots(intent_request)['EmployeeName']
    task = get_slots(intent_request)['TaskDetails']
    deadline = get_slots(intent_request)['Deadline']
    uid = uids[name]
    asignee = 'Unknown'
    manager_id = ''
    temp = intent_request['userId'].split(':')
    if len(temp)==3: 
        asignee = unames[temp[2]]
        manager_id = temp[2]
    message = "You have been assigned a task\n"+"Task Details: "+task+"\nDeadline : "+deadline+"\nAsignee : "+asignee
    source = intent_request['invocationSource']
    params = urllib.urlencode(dict({'token':'#','channel':uid,'text':message,'as_user':'false','username':'@stratbot'}))
    req = urllib2.urlopen("https://slack.com/api/chat.postMessage?"+params)
    resp = json.loads(req.read())
    params2 = urllib.urlencode({'employee_id':uid,'task_details':task,'deadline':deadline,'manager_id':manager_id})
    req2 = urllib2.urlopen('http://training.stratbeans.com/stratbot/assign',params2)
    resp2 = json.loads(req2.read())
    if resp['ok'] and resp2['ok']=='true':
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Successfully Assigned'})
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



