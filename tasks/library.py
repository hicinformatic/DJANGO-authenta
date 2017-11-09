import urllib.request, urllib.parse, os, http.cookiejar, json, sys

appdir = os.path.abspath(os.path.join(__file__ ,"../.."))
projectdir = os.path.abspath(os.path.join(__file__ ,"../../.."))
sys.path.append(projectdir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testdjango.settings")
sys.path.append(appdir)
from apps import OverConfig

class Task:
    get = 'authenta/task/update'
    extend = 'json'
    domain = 'localhost'

    def __init__(self, task, scriptname):
        self.port = OverConfig.port
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
        url = 'http://{}:{}/{}/{}.json'.format(self.domain, self.port, self.get, self.task)

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

    def getUrl(self, url):
        return 'http://{}:{}/{}'.format(self.domain, self.port, url)

    def getConfig(self, conf, function=False):
        return getattr(OverConfig, conf)() if function else getattr(OverConfig, conf)

    def encryptCache(self, filename, plaintext):
        OverConfig.encryptCache(filename, plaintext)

    def decryptCache(self, filename):
        return OverConfig.encryptCache(filename)