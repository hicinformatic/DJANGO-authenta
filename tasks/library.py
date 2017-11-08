import urllib.request, urllib.parse, os, http.cookiejar, json

class Task:
    get = 'authenta/task/update'
    extend = 'json'

    def __init__(self, port, task, scriptname):
        self.port = port
        self.task = task
        self.scriptname = scriptname
        self.scriptdir = os.path.dirname(os.path.realpath(__file__))
        self.pid = '{}/{}.pid'.format(self.scriptdir, scriptname)
        self.writePidFile()

    def writePidFile(self):
        pid = str(os.getpid())
        f = open(self.pid, 'w')
        f.write(pid)
        f.close()

    def __del__(self):
        os.unlink(self.pid)

    def update(self, status, info=''):
        data = {'task': self.scriptname, 'status': status, 'info': '', 'error': '' }
        if status == 'error' and (info is not None or info != ''):
            data['error'] = info
        elif info is not None or info != '':
            data['info'] = info
        url = "http://localhost:{}/{}/{}.json".format(self.port, self.get, self.task)

        cj = http.cookiejar.CookieJar()
        base = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

        init = urllib.request.Request(url)
        init = base.open(init)
        init = json.loads(init.read().decode('utf-8'))

        data['csrfmiddlewaretoken'] = init['csrftoken']
        data = urllib.parse.urlencode(data).encode()
        curl = urllib.request.Request(url, data=data)
        curl = base.open(curl)
        return curl.getcode()
