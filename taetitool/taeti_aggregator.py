import taetitool.util as util


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
        util.apply_assignment_rules(taetis, self.assignment_rules)
        grouped_taetis = util.group_taetis(taetis)
        total_times = util.get_total_times(taetis)

        return date, total_times, grouped_taetis
