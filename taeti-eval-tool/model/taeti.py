# from ..util import format_time

# TODO fix import of util.format_time
def format_time(time_obj):
    return time_obj.strftime("%H:%M")


class Taeti:
    def __init__(self, time_start, time_end, description, issue=None):
        self.time_start = time_start
        self.time_end = time_end
        self.time_span = time_end - time_start
        self.description = description
        self.issue_id = None
        self.issue_description = None
        self.project = None
        self.task = None

        if issue:
            self.issue_id = issue.id
            self.issue_description = issue.description
            self.project = issue.project
            self.task = issue.task

    def __str__(self):
        if self.issue_id:
            return f'{format_time(self.time_start)} - {format_time(self.time_end)} #{self.issue_id} {self.description}'
        else:
            return f'{format_time(self.time_start)} - {format_time(self.time_end)} {self.description}'

    def __repr__(self):
        return f'Taeti({self.issue_id}, \'{self.description}\', {format_time(self.time_start)}, {format_time(self.time_end)})'
