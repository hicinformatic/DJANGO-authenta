from library import Task
import os, sys, base64

scriptname = os.path.basename(__file__)[:-3]
taskid = sys.argv[1]
task = Task(taskid, scriptname)
task.update('start', 'Started')

import urllib.request, urllib.parse, json
url = 'task/purge.json'
url = task.getUrl(url)
task.update('running', 'Delete tasks')

def purge(url, task):
    curl = urllib.request.Request(url)
    credentials = ('%s:%s' % (task.username, task.password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    curl.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
    with urllib.request.urlopen(curl) as curl:
        curl = json.loads(curl.read().decode())
        if curl['number'] > 0:
            return curl['number']+purge(url, task)
        return curl['number']
number = purge(url, task)

task.update('complete', number)