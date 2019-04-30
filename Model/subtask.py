import datetime


class SubTaskList:

    def __init__(self):
        self.items = dict()
        self.active_subtask = None

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, key, value):
        self.items[key] = value

    def add_subtask(self, description, parent, completed=False, date_created=datetime.datetime.now(), sequence=1):
        if description not in self.items:
            self.items[description] = Subtask(description, parent, completed, date_created, sequence)

    def clear(self):
        self.items = dict()
        return self


class Subtask:

    def __init__(self, description, parent, completed=False, date_created=datetime.datetime.now(), date_completed=None, is_selected=False, sequence=1):
        self.description = description
        self.completed = completed
        self.date_created = date_created
        self.date_completed = date_completed
        self.is_selected = is_selected
        self.parent = parent
        self.sequence = sequence

    def set_completed(self):
        self.completed = True

    def unset_completed(self):
        self.completed = False

    def remove_task(self):
        # TODO
        pass
