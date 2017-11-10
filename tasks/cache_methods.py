from library import Task
import os, sys

scriptname = os.path.basename(__file__)[:-3]
taskid = sys.argv[1]
task = Task(taskid, scriptname)
task.update('start', 'Started')

import urllib.request, urllib.parse, json
url = 'authenta/method.json'
url = task.getUrl(url)

task.update('running', 'Get methods')
with urllib.request.urlopen(url) as url:
    methods = json.loads(url.read().decode())
    cache = {}
    for method in methods:
        if method['method'] not in cache:
            cache[method['method']] = {}
        cache[method['method']][method['id']] = method

    for method in cache:
        text = json.dumps(cache[method], ensure_ascii=False).encode('ascii')
        task.encryptCache(method, text)

task.update('complete', 'Complete')