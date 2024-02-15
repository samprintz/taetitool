import csv
import re
from datetime import datetime, timedelta

from config import Style, project_print_order
from model.issue import Issue
from model.taeti import Taeti

TAETI_DESCRIPTION_PATTERN = '(^#(\\d{1,4})\\s?)?(.*)?'
FILE_NAME_DATE_FORMAT = '%Y%m%d'
PRINT_DATE_FORMAT = '%d.%m.%Y'


def parse_date(path):
    date_string = path.split("/")[-1].split("-")[0]

    try:
        parsed_date = datetime.strptime(date_string, FILE_NAME_DATE_FORMAT)
        return parsed_date.strftime(PRINT_DATE_FORMAT)
    except ValueError:
        return None


def parse_time(time_str):
    return datetime.strptime(time_str, '%H:%M')


def format_time(time_obj):
    return time_obj.strftime('%H:%M')


def format_timedelta(time_obj):
    sec = time_obj.seconds
    hours = sec // 3600
    minutes = (sec // 60) - (hours * 60)
    return f'{hours}:{"{:02}".format(int(minutes))}'


def format_timedelta_quarterly(time_obj):
    sec = time_obj.seconds
    hours = sec // 3600
    minutes = (sec // 60) - (hours * 60)
    rounded_minutes = round(minutes / 15) * 15
    hours += rounded_minutes // 60
    rounded_minutes %= 60
    return f'{hours}:{"{:02}".format(int(rounded_minutes))}'


def read_project_data(path, default_project, default_task):
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

    default_issue = Issue(None, default_project, default_task, None)
    return DefaultKeyDict(default_issue, project_data)


def read_taeti_data(path):
    taeti_data = []

    with open(path, 'r') as file:
        for i, line in enumerate(file):
            # split by two or more whitespace characters
            col = re.split('\\s\\s+', line)
            if len(col) < 3:
                raise Exception(f'Corrupt entry in line {i}: "{line}"')
            time_start, time_end, description = col

            taeti_data.append({
                'time_start': parse_time(time_start),
                'time_end': parse_time(time_end),
                'description': description.strip()
            })

    return taeti_data


def build_taetis(taeti_data, project_data):
    # TODO merge read_taeti_data()?
    taetis = []

    for taeti_entry in taeti_data:
        description_match = re.search(TAETI_DESCRIPTION_PATTERN,
                                      taeti_entry['description'])

        issue_id = description_match.group(2)
        description = description_match.group(3)

        if issue_id:
            issue = project_data[issue_id]
            taeti = Taeti(taeti_entry['time_start'], taeti_entry['time_end'],
                          description, issue)
        else:
            taeti = Taeti(taeti_entry['time_start'], taeti_entry['time_end'],
                          description)

        taetis.append(taeti)

    return taetis


def set_special_projects_and_tasks(taetis, assignments):
    for assignment in assignments:
        filtered_taetis = [t for t in taetis if assignment['function'](t)]
        for taeti in filtered_taetis:
            taeti.project = assignment['project']
            taeti.task = assignment['task']


def get_total_times(taetis):
    first_entry = sorted(taetis, key=lambda t: t.time_start)[0]
    last_entry = sorted(taetis, key=lambda t: t.time_start, reverse=True)[0]
    day_total_time = last_entry.time_end - first_entry.time_start
    return first_entry.time_start, last_entry.time_end, day_total_time


def group_taetis_by(grouped_taetis, taetis, attributes):
    attribute, *attributes = attributes

    for taeti in taetis:
        key = getattr(taeti, attribute)
        if key not in grouped_taetis:
            grouped_taetis[key] = {
                'taetis': [],
                'grouped_taetis': {},
                'time': timedelta(0)
            }

        grouped_taetis[key]['taetis'].append(taeti)
        grouped_taetis[key]['time'] = (grouped_taetis[key]['time']
                                       + taeti.time_span)

    if len(attributes) > 0:
        for key, group in grouped_taetis.items():
            group_taetis_by(group['grouped_taetis'], group['taetis'],
                            attributes)

    return grouped_taetis


def group_taetis(taetis):
    return group_taetis_by({}, taetis, [
        'project', 'task', 'issue_description', 'issue_id'
    ])


def print_project_group(title, project_group):
    print(f'{Style.PROJECT}{format_timedelta_quarterly(project_group["time"])} '
          f'{title}{Style.ENDC}')

    for task, task_group in project_group['grouped_taetis'].items():
        if task:
            print(f'\t{format_timedelta(task_group["time"])} {task}')

        for issue_description, issue_description_group in task_group[
            'grouped_taetis'].items():
            if issue_description:
                print(
                    f'\t\t{format_timedelta(issue_description_group["time"])} '
                    f'{issue_description}')

            for issue_id, issue_id_group in issue_description_group[
                'grouped_taetis'].items():
                if issue_id:
                    print(f'\t\t\t{format_timedelta(issue_id_group["time"])} '
                          f'#{issue_id}')

                for taeti in issue_id_group['taetis']:
                    print(f'\t\t\t\t{Style.ISSUE}{str(taeti)}{Style.ENDC}')


def print_taetis(date, total_times, grouped_taetis):
    print(f'{Style.BOLD}{date}{Style.ENDC}')

    day_start_time, day_end_time, day_total_time = total_times
    print(f'{Style.BOLD}{format_time(day_start_time)} - '
          f'{format_time(day_end_time)}{Style.ENDC} '
          f'({format_timedelta(day_total_time)})\n')

    for project in project_print_order:
        project_group = grouped_taetis.pop(project)
        print_project_group(project, project_group)

    for project, project_group in grouped_taetis.items():
        print_project_group(project, project_group)
