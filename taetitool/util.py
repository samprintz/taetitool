import csv
import os.path
from datetime import datetime, timedelta
import re

from taetitool.model.issue import Issue
from taetitool.model.taeti import Taeti

TAETI_DESCRIPTION_PATTERN = '(^#(\\d{1,4})\\s?)?(.*)?'
FILE_NAME_DATE_FORMAT = '%Y%m%d'
PRINT_DATE_FORMAT = '%A, %d.%m.%Y'


class DefaultKeyDict(dict):
    def __init__(self, default_key, *args, **kwargs):
        self.default_key = default_key
        super(DefaultKeyDict, self).__init__(*args, **kwargs)

    def __missing__(self, key):
        issue = self.default_key
        issue.id = key
        return issue


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


def load_issue_data(issue_title_file_path, project_data_file_path,
                    default_project, default_task):
    if not os.path.isfile(issue_title_file_path):
        print(f'Issue title data file not found: "{issue_title_file_path}"')
        exit(0)

    if not os.path.isfile(project_data_file_path):
        print(f'Project data file not found: "{project_data_file_path}"')
        exit(0)

    issue_titles = read_issue_titles(issue_title_file_path)
    project_data = read_project_data(project_data_file_path)

    return build_issue_dict(issue_titles,
                            project_data,
                            default_project,
                            default_task)


def read_issue_titles(path):
    issue_titles = {}

    with open(path, 'r') as file:
        csv_file = csv.reader(file, delimiter=',')
        for line in csv_file:
            try:
                issue_id = line[0]
                title = line[1]

            except Exception as e:
                print(f'Error in {line}')
                raise e

            issue_titles[issue_id] = title

    return issue_titles


def read_project_data(path):
    project_data = {}

    with (open(path, 'r') as file):
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

            project_data[issue_id] = {
                "issue_id": issue_id,
                "project": project,
                "task": task,
                "description": description
            }

    return project_data


def build_issue_dict(issue_titles, project_data, default_project, default_task):
    issue_dict = {}

    for issue_id, issue in project_data.items():

        issue_title = None

        if issue_id in issue_titles.keys():
            issue_title = issue_titles[issue_id]

        issue_dict[issue_id] = Issue(issue_id,
                                     issue_title,
                                     issue["project"],
                                     issue["task"],
                                     issue["description"])

    for issue_id, issue_title in issue_titles.items():
        if issue_id not in issue_dict:
            issue_dict[issue_id] = Issue(issue_id,
                                         issue_titles[issue_id],
                                         default_project,
                                         default_task,
                                         None)

    default_issue = Issue(None, None, default_project, default_task, None)
    return DefaultKeyDict(default_issue, issue_dict)


def read_taeti_data(path):
    taeti_data = []

    with open(path, 'r') as file:
        for i, line in enumerate(file):
            if len(line.strip()):
                # split by two or more whitespace characters
                col = re.split('\\s\\s+', line)
                if len(col) != 3:
                    raise Exception(f'Corrupt entry in line {i + 1}: "{line}"')
                time_start, time_end, description = col

                taeti_data.append({
                    'time_start': parse_time(time_start),
                    'time_end': parse_time(time_end),
                    'description': description.strip()
                })

    return taeti_data


def parse_assignment_rules(rules):
    rule_names = set()
    for option, _ in rules:
        rule_name = option.split('_')[1]
        rule_names.add(rule_name)

    rule_fields = ['attribute', 'pattern', 'project', 'task']

    assigment_rules = []
    for rule_name in rule_names:
        assigment_rule = {
            'name': rule_name
        }

        for rule_field in rule_fields:
            rule_field_value = next(
                (y for x, y in rules if rule_name in x and rule_field in x),
                None)
            assigment_rule[rule_field] = rule_field_value

        assigment_rules.append(assigment_rule)

    return assigment_rules


def build_taetis(taeti_data, project_data):
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


def apply_assignment_rules(taetis, rules):
    for rule in rules:
        pattern = re.compile(rule['pattern'])
        for taeti in taetis:
            attribute = getattr(taeti, rule['attribute'])
            if attribute and pattern.match(attribute):
                taeti.project = rule['project']
                taeti.task = rule['task']


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
