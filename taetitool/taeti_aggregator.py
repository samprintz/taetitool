from datetime import timedelta
import re

import taetitool.util as util
from taetitool.taeti_aggregation import TaetiAggregation


class TaetiAggregator:
    def __init__(self, issue_data, assignment_rules):
        self.issue_data = issue_data
        self.assignment_rules = assignment_rules

    def process(self, taeti_file_path):
        taeti_data = util.read_taeti_data(taeti_file_path)

        if len(taeti_data) == 0:
            print(f'No taeti records found')
            exit(0)

        date = util.parse_date(taeti_file_path)
        taetis = util.build_taetis(taeti_data, self.issue_data)
        self.apply_assignment_rules(taetis, self.assignment_rules)
        grouped_taetis = self.group_taetis(taetis)
        total_times = self.calc_total_times(taetis)

        return TaetiAggregation(date, total_times, grouped_taetis)

    def apply_assignment_rules(self, taetis, rules):
        for rule in rules:
            pattern = re.compile(rule['pattern'])
            for taeti in taetis:
                attribute = getattr(taeti, rule['attribute'])
                if attribute and pattern.match(attribute):
                    taeti.project = rule['project']
                    taeti.task = rule['task']

    def calc_total_times(self, taetis):
        first_entry = sorted(taetis, key=lambda t: t.time_start)[0]
        last_entry = sorted(taetis, key=lambda t: t.time_start, reverse=True)[0]
        day_total_time = last_entry.time_end - first_entry.time_start
        return first_entry.time_start, last_entry.time_end, day_total_time

    def group_taetis(self, taetis):
        return self.group_taetis_by({}, taetis, [
            'project', 'task', 'issue_description', 'issue_id'
        ])

    def group_taetis_by(self, grouped_taetis, taetis, attributes):
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
                self.group_taetis_by(group['grouped_taetis'], group['taetis'],
                                     attributes)

        return grouped_taetis
