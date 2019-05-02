import datetime


class SubTaskList:

    def __init__(self):
        self.items = dict()
        self.active_subtask = None

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, key, value):
        self.items[key] = value

    def __len__(self):
        return len(self.items)

    def add_subtask(self, description, parent, completed=False, date_created=datetime.datetime.now(), sequence=1):
        if description not in self.items:
            self.items[description] = Subtask(description, parent, completed, date_created, sequence=sequence)

    def remove_subtask(self, subtask_primary):
        seq = self.items[subtask_primary].sequence
        del self.items[subtask_primary]
        for _, obj in self.items.items():
            if obj.sequence > seq:
                obj.sequence -= 1

    def modify_subtask(self, subtask_primary: str,
                       description: str, completed: bool, selected: bool):
        if description is not None:
            if description in self.items:
                return
            data_subtask = self.items[subtask_primary]
            data_subtask.description = description
            del self.items[subtask_primary]
            self.items[description] = data_subtask
            subtask_primary = description
        if completed is not None:
            self.items[subtask_primary].completed = completed
        if selected is not None:
            # TODO
            self.items[subtask_primary].selected = selected

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
