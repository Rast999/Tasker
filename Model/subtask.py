import datetime


class Subtask:

    def __init__(self, description, parent, completed=False, date_created=datetime.datetime.now(), date_completed=None, is_selected=False):
        self.description = description
        self.completed = completed
        self.date_created = date_created
        self.date_completed = date_completed
        self.is_selected = is_selected
        self.parent = parent

    def set_completed(self):
        self.completed = True

    def unset_completed(self):
        self.completed = False

    def remove_task(self):
        pass
