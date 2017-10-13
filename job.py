from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _

from .apps import AuthentaConfig
from .models import Task, Method

from datetime import datetime, timedelta
import json, subprocess, sys, urllib.parse

class Task(object):
    def __init__(self, command, task, contenttype, message):
        self.statusOrder = [AuthentaConfig.status[1][0], AuthentaConfig.status[2][0], AuthentaConfig.status[3][0]]
        self.command = command
        self.task = task
        self.contenttype = contenttype
        self.message = urllib.parse.unquote_plus(message) if message != '' else None
        self.script = None
        self.delta = None
        self.job = None

    def checkTask(task):
        check = '{0} {1}/{2}{3} {4} {5}'.format(
            AuthentaConfig.binary,
            AuthentaConfig.dir_task,
            AuthentaConfig.tasks[0][0],
            AuthentaConfig.backext, task, 
            AuthentaConfig.killscript)
        try:
            subprocess.check_call(check, shell=True)
        except subprocess.CalledProcessError:
            return False
        return True

    def startTask(task):
        bgtask = '{0} {1} {2}/{3}.py {4} {5}'.format(
            AuthentaConfig.backstart,
            AuthentaConfig.python,
            AuthentaConfig.dir_task,
            AuthentaConfig.tasks[int(task)][0],
            AuthentaConfig.port, AuthentaConfig.backend)
        try:
            subprocess.check_call(bgtask, shell=True)
        except subprocess.CalledProcessError:
            return False
        return True

    def getScript(self):
        try: 
            self.script = AuthentaConfig.tasks[int(task)][0]
            return True
        except NameError: 
            self.error = _('Task not found')
        return False

    def getDelta(self):
        try:
            self.delta = AuthentaConfig.deltas[self.script]
            return True
        except NameError:
            self.error = _('Delta not found')
        return False

    def getJob(self, status):
        try:
            if isinstance(delta, int):
                if self.delta > 40: delta = datetime.today() - timedelta(seconds=self.delta)
                else: self.delta = datetime.today() - timedelta(days=self.delta)
                self.job = Task.objects.get(task=self.script, status__in=status, dateupdate__gte=self.delta)
            elif self.delta == 'Monthly':
                self.job = Task.objects.get( task=self.script, status__in=status, dateupdate__year=datetime.now().year, dateupdate__month=datetime.now().month)
            elif self.delta == 'Annually':
                self.job = Task.objects.get(task=self.script, status__in=status, dateupdate__year=datetime.now().year)
            else:
                self.error = _('Delta not available')
                return False
        except Task.DoesNotExist:
            self.job = Task(task=self.script)
            self.job.status = AuthentaConfig.status[1][0]
        return True

    def order(self):
        if not self.getScript(): return False
        if not self.getDelta(): return False
        if not self.getJob(statusOrder): return False
        self.job.info = self.message
        self.job.save()