from Model.subtask import Subtask, SubTaskList

class TaskList:

    def __init__(self):
        self.items = dict()
        self.active_task = None

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, key, value):
        self.items[key] = value

    def __len__(self):
        return len(self.items)

    def add_task(self, description, completed=False, sequence=1):
        if description not in self.items:
            self.items[description] = Task(description, completed, sequence=sequence)

    def remove_task(self, description):
        seq = self.items[description].sequence
        del self.items[description]
        for _, obj in self.items.items():
            if obj.sequence > seq:
                obj.sequence -= 1

    def modify_task(self, primary_k: str, description: str, completed: str, selected: bool):
            if description is not None:
                if description in self.items:
                    return
                data = self.items[primary_k]
                del self.items[primary_k]
                self.items[description] = data
                primary_k = description
            if completed is not None:
                self.items[primary_k].completed = completed
            if selected is not None:
                # TODO
                self.items[primary_k].selected = selected

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

