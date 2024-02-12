class Issue:
    def __init__(self, id, project, task=None, description=None):
        self.id = id
        self.project = project
        self.task = task
        self.description = description

    def __repr__(self):
        return f'Issue({self.id}, {self.project}, {self.task}, {self.description})'
