from library import Task
import sys

taskid = 1
port = sys.argv[1]

task = Task('generate_cache')
task.taskme(port, 'start', taskid, 'startca')
task.taskme(port, 'running', taskid, 'run ca')
task.taskme(port, 'complete', taskid, 'complete ca')

task.deletePidFile()