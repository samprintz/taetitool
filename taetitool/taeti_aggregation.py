from taetitool.config import Style
import taetitool.util as util


class TaetiAggregation:
    indent_chars = '  '
    additional_taeti_indent = 1

    def __init__(self, date, total_times, taetis):
        self.date = date
        self.day_start_time, self.day_end_time, self.day_total_time = total_times
        self.taetis = taetis

    def to_string(self, project_print_order):
        print(f'{Style.BOLD}{self.date}{Style.END}')

        print(f'{Style.BOLD}{util.format_time(self.day_start_time)} - '
              f'{util.format_time(self.day_end_time)}{Style.END} '
              f'({util.format_timedelta_quarterly(self.day_total_time)})\n')

        # TODO make configurable
        group_format_defs = [
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
                self.group_to_string(project, project_group, group_format_defs)

        for project, project_group in self.taetis.items():
            self.group_to_string(project, project_group, group_format_defs)

    def group_to_string(self, title, group, group_format_defs):
        group_format_def, *group_format_defs = group_format_defs

        indent = group_format_def['indent'] * self.indent_chars

        time = util.format_timedelta(group['time'])

        if group_format_def['quarterly_time']:
            time = util.format_timedelta_quarterly(group['time'])

        if title and group_format_def['title']:
            print(indent + group_format_def['title'] % (time, title))

        for subgroup_title, subgroup in group['grouped_taetis'].items():
            self.group_to_string(subgroup_title, subgroup, group_format_defs)

        if group_format_def['taeti']:
            taeti_indent = (group_format_def['indent']
                            + self.additional_taeti_indent) * self.indent_chars
            for taeti in group['taetis']:
                print(taeti_indent + group_format_def['taeti'] % taeti)

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

    def group_to_json(self, json, group):
        for title, subgroup in group.items():
            title = str(title) if title else 'None'

            json[title] = {
                'time': int(subgroup['time'].total_seconds())
            }

            self.group_to_json(json[title], subgroup['grouped_taetis'])
