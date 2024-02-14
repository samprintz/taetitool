import re

break_re = re.compile('Break|^Private:.*')
meeting_re = re.compile('Daily|Weekly|Sprint Retrospektive|Product Management Round Table')

project_assignments = [
    {
        'function': lambda taeti: break_re.match(taeti.description),
        'project': 'Break',
        'task': 'Break'
    },
    {
        'function': lambda taeti: meeting_re.match(taeti.description),
        'project': 'Internal tasks',
        'task': 'Meeting'
    },
    {
        'function': lambda taeti: taeti.project == 'Support',
        'project': "External tasks",
        'task': 'Support'
    }
]

project_print_order = ['Break', 'Interne Tätigkeiten', 'Externe Tätigkeiten']


class Style:
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ISSUE = '\033[90m'
    PROJECT = '\033[4m'
