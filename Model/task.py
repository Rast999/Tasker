from subtask import Subtask, SubTaskList

class TaskList:

    def __init__(self):
        self.items = dict()
        self.active_task = None

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, key, value):
        self.items[key] = value

    def add_task(self, description, completed=False, sequence=1):
        if description not in self.items:
            self.items[description] = Task(description, completed, sequence=sequence)

    def clear(self):
        self.items = dict()
        return self

class Task:

    def __init__(self, description, completed=False, selected=False, sequence=1):
        self.description = description
        self.subtasks = SubTaskList()
        self.completed = completed
        self.is_selected = selected
        self.sequence = sequence

    def is_completed(self):
        return self.completed

    def set_completed(self):
        self.completed = True

    def add_subtask(self, description):
        self.subtasks.append(Subtask(description))

