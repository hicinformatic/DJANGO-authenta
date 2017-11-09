from library import Task
import os, sys

scriptname = os.path.basename(__file__)[:-3]

taskid = sys.argv[1]
task = Task(taskid, scriptname)
task.update('start', 'Started')

url = 'authenta/method.json'
import urllib.request, urllib.parse, json
url = task.getUrl(url)

task.update('running', 'Get methods')
with urllib.request.urlopen(url) as url:
    methods = json.loads(url.read().decode())
    cache = {}
    for method in methods:
        if method['method'] not in cache:
            cache[method['method']] = {}
        cache[method['method']][method['id']] = method

    task.update('running', 'Make cache')
    for method in cache:
        with open('{}/{}.json'.format(task.getConfig('dir_json'), method), 'w') as outfile:
            json.dump(cache[method], outfile, indent=4, ensure_ascii=False)

task.update('complete', 'Complete')