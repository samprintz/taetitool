import csv
import re
from datetime import datetime

from model.issue import Issue
from model.taeti import Taeti

TAETI_DESCRIPTION_PATTERN = '(^#(\\d{1,4})\\s?)?(.*)?'


def read_project_data(path, default_project):
    class DefaultKeyDict(dict):
        def __init__(self, default_key, *args, **kwargs):
            self.default_key = default_key
            super(DefaultKeyDict, self).__init__(*args, **kwargs)

        def __missing__(self, key):
            issue = self.default_key
            issue.id = key
            return issue

    project_data = {}

    with open(path, 'r') as file:
        csv_file = csv.reader(file, delimiter=',')
        for line in csv_file:
            try:
                issue_id = line[0]
                project = line[1]

                task = ''
                if len(line) >= 3:
                    task = line[2]

                description = ''
                if len(line) >= 4:
                    description = line[3]

            except Exception as e:
                print(f'Error in {line}')
                raise e
            project_data[issue_id] = Issue(issue_id, project, task, description)

    default_issue = Issue(None, default_project, None, None)
    return DefaultKeyDict(default_issue, project_data)


def read_taeti_data(path):
    taeti_data = []

    with open(path, 'r') as file:
        for i, line in enumerate(file):
            col = re.split('\\s\\s+', line)  # split by two or more whitespace characters
            if len(col) < 3:
                raise Exception(f'Corrupt entry in line {i}: "{line}"')
            time_start, time_end, description = col

            taeti_data.append({
                'time_start': parse_time(time_start),
                'time_end': parse_time(time_end),
                'description': description.strip()
            })

    return taeti_data


def parse_time(time_str):
    return datetime.strptime(time_str, '%H:%M')


def format_time(time_obj):
    return time_obj.strftime("%H:%M")


def build_taetis(taeti_data, project_data):
    # TODO merge read_taeti_data()?
    taetis = []

    for taeti_entry in taeti_data:
        description_match = re.search(TAETI_DESCRIPTION_PATTERN, taeti_entry["description"])

        issue_id = description_match.group(2)
        description = description_match.group(3)

        if issue_id:
            issue = project_data[issue_id]
            taeti = Taeti(taeti_entry["time_start"], taeti_entry["time_end"], description, issue)
        else:
            taeti = Taeti(taeti_entry["time_start"], taeti_entry["time_end"], description)

        taetis.append(taeti)

    return taetis


def set_special_projects_and_tasks(taetis, assignments):
    for assignment in assignments:
        filtered_taetis = [t for t in taetis if assignment['function'](t)]
        for taeti in filtered_taetis:
            taeti.project = assignment['project']
            taeti.task = assignment['task']
