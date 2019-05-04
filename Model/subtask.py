import datetime


class SubTaskList:

    def __init__(self):
        self.items = dict()
        self.active_subtask = None
        self.items_sorted = sorted(list(self.items.values()))

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, key, value):
        self.items[key] = value

    def __len__(self):
        return len(self.items)

    def add_subtask(self, description, parent, completed=False, date_created=datetime.datetime.now(), sequence=1):
        if description not in self.items:
            item = Subtask(description, parent, completed, date_created, sequence=sequence)
            self.items[description] = item
            self.items_sorted.append(item)


    def remove_subtask(self, subtask_primary):
        seq = self.items[subtask_primary].sequence
        del self.items[subtask_primary]
        if self.items_sorted[seq - 1].description == subtask_primary:
            self.items_sorted.pop(seq - 1)
        else:
            raise ValueError("Subtask list is not alligned")
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
            self.items[subtask_primary].selected = selected
        # modify the subtask in sorted_list too
        seq = self.items[subtask_primary].sequence
        self.items_sorted[seq - 1] = self.items[subtask_primary]

    def clear(self):
        self.items = dict()
        return self

    def sort_items(self):
        self.items_sorted.sort()


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

    def __lt__(self, other):
        return self.sequence < other.sequence

    def __str__(self):
        result = "description: %s\ncompleted: %s\ndate created: %s\nselected: %s\nsequence: %s\n"
        return result % (self.description, self.completed, self.date_created, self.is_selected, self.sequence)


if __name__ == '__main__':
    subtask_list = []
    subtask_list.append(Subtask("s 1", None, sequence=5))
    subtask_list.append(Subtask("s 2", None, sequence=1))
    subtask_list.append(Subtask("s 3", None, sequence=3))
    subtask_list.append(Subtask("s 4", None, sequence=15))
    subtask_list.append(Subtask("s 5", None, sequence=90))
    subtask_list.append(Subtask("s 6", None, sequence=44))
    subtask_list.append(Subtask("s 7", None, sequence=8))
    subtask_list.append(Subtask("s 8", None, sequence=22))
    subtask_list.sort()
    for subtask  in subtask_list:
        print(subtask)
