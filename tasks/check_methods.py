from library import Task
import os, sys, urllib.request, urllib.parse, http.cookiejar, json


scriptname = os.path.basename(__file__)[:-3]
taskid = sys.argv[1]
task = Task(taskid, scriptname)
task.update('start', 'Started')

import urllib.request, urllib.parse, json
methods = 'authenta/method.json'
check = 'authenta/method/function/{}.json'

task.update('running', 'Get methods')
with urllib.request.urlopen(task.getUrl(methods)) as url:
    methods = json.loads(url.read().decode())
    infos = {}
    for method in methods:
        infos[method['id']] = {}
        checkurl = task.getUrl(check.format(method['id']))
        cj = http.cookiejar.CookieJar()
        base = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        init = urllib.request.Request(checkurl)
        init = base.open(init)
        init = json.loads(init.read().decode('utf-8'))
        data = { 'function': 'check', }
        data['csrfmiddlewaretoken'] = init['csrftoken']
        data = urllib.parse.urlencode(data).encode()
        try:
            curl = urllib.request.Request(checkurl, data=data)
            curl = base.open(curl)
            print(curl.read())
            infos[method['id']]['status'] = curl.getcode()
        except Exception as e:
            infos[method['id']]['error'] = str(e)
    
task.update('complete', json.dumps(infos))