from library import Task
import os, sys

scriptname = os.path.basename(__file__)[:-3]
taskid = sys.argv[1]
task = Task(taskid, scriptname)
task.update('start', 'Started')

import urllib.request, urllib.parse, json
url = 'methods.json'
url = task.getUrl(url)
task.update('running', 'Get methods')

with urllib.request.urlopen(url) as url:
    methods = json.loads(url.read().decode())
    cache = {}
    for method in methods:
        if method['method'] not in cache:
            cache[method['method']] = []
        cache[method['method']].append(method)

    dir_cache = task.getConfig('App', 'dir_cache')
    for method in cache:
        with open('{}/{}.json'.format(dir_cache, method), 'w') as cache_file:
            json.dump(cache[method], cache_file, indent=4, ensure_ascii=False)
        cache_file.closed

task.update('complete', 'Complete')