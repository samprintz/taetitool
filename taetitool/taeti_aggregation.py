from taetitool.config import Style
from taetitool.util import format_timedelta_quarterly, format_timedelta, \
    format_time


class TaetiAggregation:
    def __init__(self, date, total_times, taetis):
        self.date = date
        self.day_start_time, self.day_end_time, self.day_total_time = total_times
        self.taetis = taetis

    @staticmethod
    def print_project_group(title, project_group):
        print(
            f'{Style.UNDERLINE}{format_timedelta_quarterly(project_group["time"])} '
            f'{title}{Style.END}')

        for task, task_group in project_group['grouped_taetis'].items():
            if task:
                print(
                    f'  {format_timedelta(task_group["time"])} {Style.BOLD}{task}{Style.END}')

            for issue_description, issue_description_group in task_group[
                'grouped_taetis'].items():
                if issue_description:
                    print(
                        f'    {format_timedelta(issue_description_group["time"])} '
                        f'{issue_description}')

                for issue_id, issue_id_group in issue_description_group[
                    'grouped_taetis'].items():
                    if issue_id:
                        print(
                            f'      {format_timedelta(issue_id_group["time"])} '
                            f'#{issue_id}')

                    for taeti in issue_id_group['taetis']:
                        print(f'        {Style.GREY}{str(taeti)}{Style.END}')

    def to_string(self, project_print_order):
        print(f'{Style.BOLD}{self.date}{Style.END}')

        print(f'{Style.BOLD}{format_time(self.day_start_time)} - '
              f'{format_time(self.day_end_time)}{Style.END} '
              f'({format_timedelta_quarterly(self.day_total_time)})\n')

        for project in project_print_order:
            if project in self.taetis:
                project_group = self.taetis.pop(project)
                self.print_project_group(project, project_group)

        for project, project_group in self.taetis.items():
            self.print_project_group(project, project_group)

    def to_json(self):
        taetis = {}

        for project, project_group in self.taetis.items():
            project = project if project else 'None'
            taetis[project] = {
                'time': int(project_group['time'].total_seconds())
            }

            for task, task_group in project_group['grouped_taetis'].items():
                task = task if task else 'None'
                taetis[project][task] = {
                    'time': int(project_group['time'].total_seconds())
                }

                for issue_description, issue_description_group in task_group[
                    'grouped_taetis'].items():
                    issue_description = issue_description if issue_description else 'None'
                    taetis[project][task][issue_description] = {
                        'time': int(project_group['time'].total_seconds())
                    }

                    for issue_id, issue_id_group in issue_description_group[
                        'grouped_taetis'].items():
                        issue_id = str(issue_id) if issue_id else 'None'
                        taetis[project][task][issue_description][
                            issue_id] = {
                            'time': int(project_group['time'].total_seconds())
                        }

        return {
            'date': self.date,
            'day_end_time': self.day_end_time,
            'day_start_time': self.day_start_time,
            'day_total_time': int(self.day_total_time.total_seconds()),
            'taetis': taetis
        }
