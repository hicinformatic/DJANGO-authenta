from library import Task
import os, sys, urllib.request, urllib.parse, http.cookiejar, json, base64


scriptname = os.path.basename(__file__)[:-3]
taskid = sys.argv[1]
task = Task(taskid, scriptname)
task.update('start', 'Started')


import urllib.request, urllib.parse, json
methods = task.getUrl('methods.json')
check = 'method/check/{}.json'

task.update('running', 'Get methods')

curl = urllib.request.Request(methods)
credentials = ('%s:%s' % (task.username, task.password))
encoded_credentials = base64.b64encode(credentials.encode('ascii'))
curl.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
with urllib.request.urlopen(curl) as url:
    methods = json.loads(url.read().decode())
    infos = {}
    for method in methods:
        infos[method['id']] = {}
        checkurl = task.getUrl(check.format(method['id']))
        try:
            curl = urllib.request.Request(checkurl)
            curl.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
            curl = urllib.request.urlopen(curl)
            infos[method['id']]['status'] = curl.getcode()
            data = json.loads(curl.read().decode())
            infos[method['id']]['name'] = data['name']
            infos[method['id']]['error'] = data['error']
        except Exception as e:
            infos[method['id']]['error'] = str(e)
 
task.update('complete', json.dumps(infos))