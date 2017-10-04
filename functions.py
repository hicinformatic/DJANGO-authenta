from django.shortcuts import render

from .apps import AuthentaConfig
from .models import Task, Method

# ------------------------------------------- #
# CONTENT TYPE - PROXY
# ------------------------------------------- #
# Content type orientation
# ------------------------------------------- #
def responseKO(contenttype, task, code, error):
    if contenttype == 'txt':
        tpl = _('status: KO\ntask: {ntask}\nname: {name}\ntechnical: {technical}\ncode: {code}\nerror: {error}')
        datas = {'task': task, 'name': AuthentaConfig.tasks[int(task)][0], 'technical': AuthentaConfig.tasks[int(task)][1], 'code': code, 'error': error}
        return HttpResponse(tpl.format(**datas), status_code=code, content_type=AuthentaConfig.contenttype_txt)
    if contenttype == 'json': 
        datas = { 'task': task, 'name': AuthentaConfig.tasks[int(task)][0], 'technical': AuthentaConfig.tasks[int(task)][1], 'code': code, 'error': error}
        return JsonResponse(datas, safe=False)
    else:
        tpl = _('status: KO\ntask: {ntask}\nname: {name}\ntechnical: {technical}\ncode: {code}\nerror: {error}')
        datas = { 'task': task, 'name': AuthentaConfig.tasks[int(task)][0], 'technical': AuthentaConfig.tasks[int(task)][1], 'code': code, 'error': error}
        return render(request, 'Authenta/failed.html', context=datas)

def responseOK(contenttype, task, message):
    if contenttype == 'txt':
        tpl = _('status: KO\ntask: {task}\nname: {name}\ntechnical: {technical}\nmessage: {message}')
        datas = {'task': task, 'name': AuthentaConfig.tasks[int(task)][0], 'technical': AuthentaConfig.tasks[int(task)][1], 'message': message}
        return HttpResponse(tpl.format(**datas), content_type=AuthentaConfig.contenttype_txt)
    if contenttype == 'json':
        datas = { 'task': task, 'name': AuthentaConfig.tasks[int(task)][0], 'technical': AuthentaConfig.tasks[int(task)][1], 'message': message}
        return JsonResponse(datas, safe=False)
    else:
        tpl = _('status: KO\ntask: {ntask}\nname: {name}\ntechnical: {technical}\nmessage: {message}')
        datas = { 'task': task, 'name': AuthentaConfig.tasks[int(task)][0], 'technical': AuthentaConfig.tasks[int(task)][1], 'code': code, 'error': error}
        return render(request, 'Authenta/success.html', context=datas)

"""
-------------------------------------------------------------------
TASK MANAGER
-------------------------------------------------------------------
Scenario type:
1-order :    Task ordered
2-start :    Task started
3-running :  Task running
4-complete : Task complete
Error encountered
0-error:     Task in error
-------------------------------------------------------------------
"""

# ------------------------------------------- #
# checkTask
# ------------------------------------------- #
# Check if the task can be ordered or started
# ------------------------------------------- #
def checkTask(task):
    check = '{0} {1}/{2}{3} {4} {5}'.format(
        AuthentaConfig.binary,
        AuthentaConfig.taskdir,
        AuthentaConfig.tasks[0][0],
        AuthentaConfig.checkext, task, 
        AuthentaConfig.killscript)
    try: subprocess.check_call(check, shell=True)
    except subprocess.CalledProcessError: return False
    return True

# ------------------------------------------- #
# startTask
# ------------------------------------------- #
# Try to start the task
# ------------------------------------------- #
def startTask(task):
    bgtask = '{0} {1} {2}/{3}.py {4} {5}'.format(
        AuthentaConfig.backstart,
        AuthentaConfig.python,
        AuthentaConfig.taskdir,
        AuthentaConfig.tasks[int(task)][0],
        AuthentaConfig.port, AuthentaConfig.backend)
    try: subprocess.check_call(bgtask, shell=True)
    except subprocess.CalledProcessError: return False
    return True

# ------------------------------------------- #
# error
# ------------------------------------------- #
# Task in error
# ------------------------------------------- #
def error(contenttype, task, error):
    try: script = AuthentaConfig.tasks[int(task)][0]
    except NameError: return responseKO('html', task, 404, _('Task not found'))
    try: thetask = Task.objects.filter(task=script, status__in=['order', 'start', 'running']).latest('dateupdate')
    except Task.DoesNotExist: return responseKO(contenttype, task, 403,  _('No task'))
    thetask.status = 'error'
    if error is None or error == '': thetask.error = _('Error')
    else: thetask.error = error
    thetask.save()
    return responseOK(contenttype, task, error)

# ------------------------------------------- #
# order
# ------------------------------------------- #
# Order a task
# ------------------------------------------- #
def order(contenttype, task, message):
    try: script = AuthentaConfig.tasks[int(task)][0]
    except NameError: return responseKO('html', task, 404, _('Task not found'))
    try: delta = cAuthentaConfig.deltas[script]
    except NameError: return responseKO('html', task, 404, _('Delta not found'))
    try:
        if isinstance(delta, int):
            if delta > 40: delta = datetime.today() - timedelta(seconds=delta)
            else:            delta = datetime.today() - timedelta(days=delta)
            thetask = Task.objects.get(task=script, status__in=['order', 'start', 'running'], dateupdate__gte=delta)
        elif delta == 'Monthly':
            thetask = Task.objects.get(task=script, status__in=['order', 'start', 'running'], dateupdate__year=datetime.now().year, dateupdate__month=datetime.now().month)
        elif delta == 'Annually':
            thetask = Task.objects.get(task=script, status__in=['order', 'start', 'running'], dateupdate__year=datetime.now().year)
        else:
            return responseKO(contenttype, task, 403, _('Delta not available'))
    except Task.DoesNotExist:
        thetask = Task(task=script)
        if message is not None or message != '': thetask.info = message
        thetask.save()
    if thetask.status >= 1:
        if checkTask(script) is True:
            if startTask(task) is True:
                return responseOK(contenttype, task, message)
            return responseKO(contenttype, task, 403, _('Task can\'t be started'))
        return responseKO(contenttype, task, 403,  _('Task already running'))
    else:
        return responseKO(contenttype, task, 403, _('Delta too short please wait'))    
    return responseKO(contenttype, task, 403, _('Task can\'t be started'))

# ------------------------------------------- #
# start
# ------------------------------------------- #
# Start a task
# ------------------------------------------- #
def start(contenttype, task, message):
    try: script = AuthentaConfig.tasks[int(task)][0]
    except NameError: return responseKO('html', task, 404, _('Task not found'))
    try: thetask = Task.objects.filter(task=script, status=1).latest('dateupdate')
    except Task.DoesNotExist: return responseKO(contenttype, task, 403,  _('No task to start'))
    thetask.status = 2
    if message is None or message == '': thetask.info = _('Started')
    else: thetask.info = message
    thetask.save()
    return responseOK(contenttype, task, message)

# ------------------------------------------- #
# running
# ------------------------------------------- #
# Task running
# ------------------------------------------- #
def running(contenttype, task, message):
    try: script = AuthentaConfig.tasks[int(task)][0]
    except NameError: return responseKO('html', task, 404, _('Task not found'))
    try: thetask = Task.objects.filter(task=script, status__in=['start', 'running']).latest('dateupdate')
    except Task.DoesNotExist: return responseKO(contenttype, task, 403,  _('No task running'))
    thetask.status = 3
    if message is None or message == '': thetask.info = _('Running')
    else: thetask.info = message
    thetask.save()
    return responseOK(contenttype, task, message)

# ------------------------------------------- #
# complete
# ------------------------------------------- #
# Task completed
# ------------------------------------------- #
def complete(contenttype, task, message):
    try: script = AuthentaConfig.tasks[int(task)][0]
    except NameError: return responseKO('html', task, 404, _('Task not found'))
    try: thetask = Task.objects.filter(task=script, status__in=['start', 'running']).latest('dateupdate')
    except Task.DoesNotExist: return responseKO(contenttype, task, 403,  _('No task to complete'))
    thetask.status = 4
    if message is None or message == '': thetask.info = _('Complete')
    else: thetask.info = message
    thetask.save()
    return responseOK(contenttype, task, message)

# ------------------------------------------- #
# subtask
# ------------------------------------------- #
# Start any subtask
# ------------------------------------------- #
def subtask(contenttype, task, secondtask):
    try: script = AuthentaConfig.tasks[int(task)][0]
    except NameError: return responseKO(contenttype, task, 404, _('Task not found'))
    try: secondtaskname = cAuthentaConfig.subtasks[script][int(secondtask)]
    except Exception: return responseKO(contenttype, task, 404, _('Subtask not found'))
    result = getattr(sys.modules[__name__], secondtaskname)(contenttype, task, script)
    if result is True: return responseOK(contenttype, task, secondtaskname)
    else: return responseKO(contenttype, task, 500, result)