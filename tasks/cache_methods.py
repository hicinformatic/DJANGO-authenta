from library import Task
import sys, os

port = sys.argv[1]
taskid = sys.argv[2]

scriptname = os.path.basename(__file__)[:-3]

task = Task(port, taskid, scriptname)
task.update('start', 'ca demarre')
task.update('running', 'ca demarre')
task.update('complete', 'ca demarre')

