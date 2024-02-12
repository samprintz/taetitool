# from ..util import format_time

# TODO fix import of util.format_time
def format_time(time_obj):
    return time_obj.strftime("%H:%M")


class Taeti:
    def __init__(self, time_start, time_end, description, issue_id=None):
        self.time_start = time_start
        self.time_end = time_end
        self.description = description
        self.issue_id = issue_id

    def __str__(self):
        return f'{format_time(self.time_start)}\t{format_time(self.time_end)}\t{self.issue_id}\t{self.description}'

    def __repr__(self):
        return f'Taeti({self.issue_id}, \'{self.description}\', {format_time(self.time_start)}, {format_time(self.time_end)})'
