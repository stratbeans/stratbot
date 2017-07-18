import urllib
import urllib2
import MySQLdb
import json

params = urllib.urlencode(dict({'token':'#'}))
req = urllib2.urlopen("https://slack.com/api/users.list?"+params)
ulist = json.loads(req.read())
uids = {}
if ulist['ok']:
    for m in ulist['members']:
        if m['profile']['real_name']:
            uids[m['profile']['real_name']] = m['id']

db = MySQLdb.connect(host='localhost', user='', passwd='', db='')
cur = db.cursor()
for i in uids:
    cur.execute('INSERT INTO users(user_id,user_name) VALUES("%s","%s");'%(uids[i],i))
db.commit()
db.close()