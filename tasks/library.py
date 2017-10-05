import urllib.request, urllib.parse, os

class Task:
    def __init__(self, name):
        self.name = name
        self.scriptdir = os.path.dirname(os.path.realpath(__file__))
        self.pid = '{}/{}.pid'.format(self.scriptdir, self.name)
        self.writePidFile()


    def writePidFile(self):
        pid = str(os.getpid())
        f = open(self.pid, 'w')
        f.write(pid)
        f.close()

    def deletePidFile(self):
        os.unlink(self.pid)

    def error(self, port, task, message=''):
        if message is None or message == '': c = urllib.request.urlopen("http://localhost:{}/authenta/{}/{}.json/{}".format(port, 'error', taskl))
        else: c = urllib.request.urlopen("http://localhost:{}/authenta/{}/{}.json/{}".format(port, 'error', task, urllib.parse.quote_plus(message)))
        return c.getcode()

    def taskme(self, port, command, task, message=''):
        if message is None or message == '': c = urllib.request.urlopen("http://localhost:{}/authenta/{}/{}.json".format(port, command, task))
        else: c = urllib.request.urlopen("http://localhost:{}/authenta/{}/{}.json/{}".format(port, command, task, urllib.parse.quote_plus(message)))
        code = c.getcode()
        if code != 200: error(port, task)
        return code