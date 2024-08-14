from taetitool.config import Style
from taetitool.util import format_timedelta_quarterly, format_timedelta, \
    format_time


class TaetiAggregation:
    indent_chars = '  '
    additional_taeti_indent = 1

    def __init__(self, date, total_times, taetis):
        self.date = date
        self.day_start_time, self.day_end_time, self.day_total_time = total_times
        self.taetis = taetis

    def to_string(self, project_print_order):
        print(f'{Style.BOLD}{self.date}{Style.END}')

        print(f'{Style.BOLD}{format_time(self.day_start_time)} - '
              f'{format_time(self.day_end_time)}{Style.END} '
              f'({format_timedelta_quarterly(self.day_total_time)})\n')

        # TODO make configurable
        level_templates = [
            {
                'quarterly_time': True,
                'title': f'{Style.UNDERLINE}%s %s{Style.END}',
                'taeti': None,
                'indent': 0,
            },
            {
                'quarterly_time': False,
                'title': f'%s {Style.BOLD}%s{Style.END}',
                'taeti': None,
                'indent': 1,
            },
            {
                'quarterly_time': False,
                'title': f'%s %s',
                'taeti': None,
                'indent': 2,
            },
            {
                'quarterly_time': False,
                'title': f'%s #%s',
                'taeti': f'{Style.GREY}%s{Style.END}',
                'indent': 3,
            }
        ]

        for project in project_print_order:
            if project in self.taetis:
                project_group = self.taetis.pop(project)
                self.group_to_string(project, project_group, level_templates)

        for project, project_group in self.taetis.items():
            self.group_to_string(project, project_group, level_templates)

    def group_to_string(self, title, group, level_templates):
        level_template, *level_templates = level_templates

        indent = level_template['indent'] * self.indent_chars

        time = format_timedelta(group['time'])

        if level_template['quarterly_time']:
            time = format_timedelta_quarterly(group['time'])

        if title and level_template['title']:
            print(indent + level_template['title'] % (time, title))

        for subgroup_title, subgroup in group['grouped_taetis'].items():
            self.group_to_string(subgroup_title, subgroup, level_templates)

        if level_template['taeti']:
            taeti_indent = (level_template['indent']
                            + self.additional_taeti_indent) * self.indent_chars
            for taeti in group['taetis']:
                print(taeti_indent + level_template['taeti'] % taeti)

    def group_to_json(self, json, group):
        for title, subgroup in group.items():
            title = str(title) if title else 'None'

            json[title] = {
                'time': int(subgroup['time'].total_seconds())
            }

            self.group_to_json(json[title], subgroup['grouped_taetis'])

    def to_json(self):
        json = {}
        self.group_to_json(json, self.taetis)

        return {
            'date': self.date,
            'day_end_time': self.day_end_time,
            'day_start_time': self.day_start_time,
            'day_total_time': int(self.day_total_time.total_seconds()),
            'taetis': json
        }
