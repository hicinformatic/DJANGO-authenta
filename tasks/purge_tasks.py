from library import Task
import os, sys

scriptname = os.path.basename(__file__)[:-3]
taskid = sys.argv[1]
task = Task(taskid, scriptname)
task.update('start', 'Started')

import urllib.request, urllib.parse, json
url = 'task/purge.json'
url = task.getUrl(url)
task.update('running', 'Delete tasks')

def purge(url):
    with urllib.request.urlopen(url) as curl:
        curl = json.loads(curl.read().decode())
        if curl['number'] > 0:
            return curl['number']+purge(url)
        return curl['number']
number = purge(url)

task.update('complete', number)