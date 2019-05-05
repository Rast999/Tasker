"""
Data schema for shelve

{
    "Task description" : {
                            "subtask description": {
                                                        "Description": "subtask description",
                                                        "Date created": 01/01/2019,
                                                        ...
                                                    },
                            "another subtask": {
                                                    "Description": "another subtask",
                                                    "Date created": 01/01/1900,
                                                    ...
                                                }
                        },
    "Another Task description": {...}
}

"""

import shelve
import datetime


class DBConnectionShelve:

    ignored_fields = ["completed", "sequence", "selected"]

    def __init__(self):
        self.db = None

    def connect(self, db_name: str):
        self.db = shelve.open(db_name)
        return self.db

    def sync(self, tasks: object):
        result = tasks.clear()
        for task in self.db.keys():
            result.add_task(task, self.db[task]["completed"], self.db[task]["sequence"])
            for subtask in self.db[task].keys():
                if subtask not in self.ignored_fields:
                    item = self.db[task][subtask]
                    result[task].subtasks.add_subtask(subtask, result[task], item["completed"], item["date_created"], item["sequence"])
            result[task].subtasks.sort_items()
        result.sort_items()
        return result

    def close_db(self):
        self.db.close()

    def add_task_to_db(self, description: str, sequence: int):
        if self.db is not None and description not in self.db:
            self.db[description] = self.db.get(description, dict())
            data = self.db[description]
            data["completed"] = False
            data["sequence"] = sequence
            self.db[description] = data

    def add_subtask_to_db(self, task: object, description: str, sequence: int):
        if self.db is not None and description not in self.db[task.description]:
            subtask = dict()
            subtask["description"] = description
            subtask["date_created"] = datetime.datetime.now()
            subtask["completed"] = False
            subtask["sequence"] = sequence
            data = self.db[task.description]
            data[description] = subtask
            self.db[task.description] = data

    def remove_task_from_db(self, primary_k):
        if self.db is not None:
            try:
                seq = self.db[primary_k]["sequence"]
                del self.db[primary_k]
                # adjust the sequence adter task deletion
                for task, subtasks in self.db.items():
                    if subtasks["sequence"] > seq:
                        data = self.db[task]
                        data["sequence"] -= 1
                        self.db[task] = data
            except KeyError:
                pass

    def remove_subtask_from_db(self, primary_k, subtask_primary):
        if self.db is not None:
            data = self.db[primary_k]
            seq = data[subtask_primary]["sequence"]
            del data[subtask_primary]
            # adjust the sequence numbers
            for desc, subtask in data.items():
                if desc not in self.ignored_fields and\
                   subtask["sequence"] > seq:
                    subtask["sequence"] -= 1
            self.db[primary_k] = data

    def modify_task(self, primary_key: str, description: str = None,
                    completed: bool = None, selected: bool = None):
        if self.db is not None:
            if description is not None:
                if description in self.db:
                    return
                data = self.db[primary_key]
                del self.db[primary_key]
                self.db[description] = data
                primary_key = description
            if completed is not None:
                data = self.db[primary_key]
                data["completed"] = completed
                self.db[primary_key] = data
            if selected is not None:
                print(primary_key)
                data = self.db[primary_key]
                data["selected"] = selected
                self.db[primary_key] = data

    def modify_subtask(self, primary_k: str, subtask_primary: str,
                       description: str = None, completed: bool = None, selected: bool = None):
            if description is not None:
                if description in self.db[primary_k]:
                    return
                data_task = self.db[primary_k]
                data_subtask = data_task[subtask_primary]
                del data_task[subtask_primary]
                data_subtask["description"] = description
                data_task[description] = data_subtask
                self.db[primary_k] = data_task
                subtask_primary = description
            if completed is not None:
                data_task = self.db[primary_k]
                data_task[subtask_primary]["completed"] = completed
                self.db[primary_k] = data_task
            if selected is not None:
                data_task = self.db[primary_k]
                data_task[subtask_primary]["selected"] = selected
                self.db[primary_k] = data_task


if __name__ == '__main__':
    D = DBConnectionShelve()
    D.connect("../data/db")
    D.add_task_to_db("test task3")
    D.add_task_to_db("second task3")
    for k, v in D.db.items():
        print(k, v)
