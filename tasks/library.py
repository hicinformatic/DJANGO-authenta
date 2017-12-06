import urllib.request, urllib.parse, os, http.cookiejar, json, sys

appdir = os.path.abspath(os.path.join(__file__ ,"../.."))
projectdir = os.path.abspath(os.path.join(__file__ ,"../../.."))
sys.path.append(projectdir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testdjango.settings")
sys.path.append(appdir)
from apps import Config as  conf

class Task:
    url_update = 'http://localhost:{port}/{namespace}/task/update/{taskidid}.{extension}'
    namespace = conf.App.namespace
    port = conf.Task.django_port
    directory = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, taskid, scriptname):
        self.taskid = taskid
        self.scriptname = scriptname
        self.file_pid = '{directory}/{taskidid}.pid'.format(directory=self.directory, taskidid=taskid)
        self.writePidFile()

    def writePidFile(self):
        f = open(self.file_pid, 'w')
        f.write(str(os.getpid()))
        f.close()

    def __del__(self):
        os.unlink(self.file_pid)

    def update(self, status, info=''):
        data = {'status': status, 'error': '', 'info': ''}
        if info is not None or info != '':
            if status == 'error': data['error'] = info
            else: data['info'] = info
        url = self.url_update.format(namespace=self.namespace, port=self.port, taskidid=self.taskid,extension='json')
        cj = http.cookiejar.CookieJar()
        base = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        init = urllib.request.Request(url)
        init = base.open(init)
        init = json.loads(init.read().decode('utf-8'))
        data['csrfmiddlewaretoken'] = init['token']
        data = urllib.parse.urlencode(data).encode()
        curl = urllib.request.Request(url, data=data)
        curl = base.open(curl)
        return curl.getcode()

    def getUrl(self, url):
        return 'http://localhost:{port}/{namespace}/{url}'.format(namespace=self.namespace, port=self.port, url=url)

    def getConfig(self, clas, attribute, function=False):
        return getattr(getattr(conf, clas), attribute)() if function else getattr(getattr(conf, clas), attribute)

    #def encryptCache(self, filename, plaintext):
    #    conf.encryptCache(filename, plaintext)

    #def decryptCache(self, filename):
    #    return conf.encryptCache(filename)