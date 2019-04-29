from .subtask import Subtask


class Task:

    def __init__(self, description, subtasks=[], completed=False, selected=False):
        self.description = description
        self.subtasks = subtasks
        self.completed = completed
        self.is_selected = selected

    def is_completed(self):
        return self.completed

    def set_completed(self):
        self.completed = True

    def add_subtask(self, description):
        self.subtasks.append(Subtask(description))

