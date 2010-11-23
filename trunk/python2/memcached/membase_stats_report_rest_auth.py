#!/usr/bin/env python
# Corey Goldberg - 2010
# print a 60 sec snapshot report of bucket statistics from Membase (Membase Management REST API)
# uses HTTP Basic Authentication



import json
import urllib2


NODE = '192.168.12.171'
PORT = '8091'
BUCKET = 'default'
USERNAME = 'Administrator'
PASSWORD = 'Secret'

DEBUG = False


password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
top_level = '%s:%s' % (NODE, PORT)
password_mgr.add_password(None, top_level, USERNAME, PASSWORD)
auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
if DEBUG:
    debug_handler = urllib2.HTTPHandler(debuglevel=1)
    opener = urllib2.build_opener(auth_handler, debug_handler)
else:
    opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)

url =  'http://%s:%s/pools/default/buckets/%s/stats?stat=opsbysecond&period=1m' % (NODE, PORT, BUCKET)

results = json.load(urllib2.urlopen(url))
 
print 'stat'.rjust(23), 'min'.rjust(15), 'avg'.rjust(15), 'max'.rjust(15)
print '-----------------------------------------------------------------------'
   
for stat_name, values in sorted(results['op']['samples'].iteritems()):
    if stat_name not in ['timestamp']:
        mn = '%.0f' % min(values)
        mx = '%.0f' % max(values)
        avg = '%.2f' % (float(sum(values)) / len(values))
        print stat_name.rjust(23), mn.rjust(15), avg.rjust(15), mx.rjust(15)

