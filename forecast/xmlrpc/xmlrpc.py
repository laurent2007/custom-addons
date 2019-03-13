## XML-RPC Library

import functools
import xmlrpc.client
HOST = '192.168.116.133'
PORT = 8069
DB = 'dev0313'
USER = 'laurent2007@163.com'
PASSWD = '860510'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

#1. Login
uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB,USER,PASSWD)
print("Logged in as %s (uid:%d)" % (USER,uid))

call = functools.partial(
    xmlrpc.client.ServerProxy(ROOT + 'object').execute,DB,uid,PASSWD)

#2. Read the Sessions
sessions = call('forecast.session','search_read',[],['name','seats'])
for session in sessions:
    print("Session %s (%s seats)" % (session['name'],session['seats']))
    
#3. Create a new Session
course_id = call('forecast.course','search',[('name','ilike','语文')])[0]
session_id = call('forecast.session','create',{
        'name' : 'My Session',
        'course_id' : course_id,
    })

