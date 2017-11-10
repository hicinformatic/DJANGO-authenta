from library import Task
import os, sys

scriptname = os.path.basename(__file__)[:-3]
taskid = sys.argv[1]
task = Task(taskid, scriptname)
task.update('start', 'Started')

import urllib.request, urllib.parse, json
url = 'authenta/task/purge.json'
url = task.getUrl(url)

task.update('running', 'Delete tasks')
with urllib.request.urlopen(url) as url:
    methods = json.loads(url.read().decode())
    print(str(methods))

task.update('complete', 'Complete')