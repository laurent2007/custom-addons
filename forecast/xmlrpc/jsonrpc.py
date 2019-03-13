##JSON-RPC Library

import json
import random
import urllib.request

HOST = '192.168.116.133'
PORT = '8069'
DB = 'dev0313'
USER = 'laurent2007@163.com'
PASSWD = '860510'


def json_rpc(url,method,params):
    data = {
        "jsonrpc":"2.0",
        "method":method,
        "params":params,
        "id":random.randint(0,10000000000),
    }
    
    req = urllib.request.Request(url=url,data=json.dumps(data).encode(),headers={
            "Content-Type":"application/json",
    })
    
    reply = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]

def call(url,service,method,*args):
    return json_rpc(url,"call",{"service":service,"method":method,"args":args})


# login in the given database
url = "http://%s:%s/jsonrpc" % (HOST,PORT)
uid = call(url,"common","login",DB,USER,PASSWD)
print(url)
# create a new course
args = {
    'name': 'New Course',
    'description': 'This is new course',
    'responsible_id':uid,
}
course_id = call(url, "object", "execute", DB, uid, PASSWD, 'forecast.forecast', 'create', args)

