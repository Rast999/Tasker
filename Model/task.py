from Model.subtask import Subtask, SubTaskList


class TaskList:

    def __init__(self):
        self.items = dict()
        self.active_task = None
        self.items_sorted = sorted(list(self.items.values()))

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, key, value):
        self.items[key] = value

    def __len__(self):
        return len(self.items)

    def add_task(self, description, completed=False, sequence=1):
        if description not in self.items:
            item = Task(description, completed, sequence=sequence)
            if self.active_task is None:
                self.active_task = item
                item.is_selected = True
            self.items[description] = item
            self.items_sorted.append(item)

    def remove_task(self, description):
        seq = self.items[description].sequence
        del self.items[description]
        if self.items_sorted[seq - 1].description == description:
            self.items_sorted.pop(seq - 1)
        else:
            raise ValueError("Task list is not alligned")
        for _, obj in self.items.items():
            if obj.sequence > seq:
                obj.sequence -= 1

    def modify_task(self, primary_k: str, description: str, completed: bool, selected: bool):
        if description is not None:
            if description in self.items:
                return
            data = self.items[primary_k]
            data.description = description
            del self.items[primary_k]
            self.items[description] = data
            primary_k = description
        if completed is not None:
            self.items[primary_k].completed = completed
        if selected is not None:
            self.items[primary_k].is_selected = selected
        seq = self.items[primary_k].sequence
        self.items_sorted[seq - 1] = self.items[primary_k]

    def clear(self):
        self.items = dict()
        return self

    def sort_items(self):
        self.items_sorted.sort()


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

    def __lt__(self, other):
        return self.sequence < other.sequence

