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

    ignored_fields = ["completed", "sequence"]

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

    def remove_task_from_db(self, task):
        if self.db is not None:
            try:
                del self.db[task]
            except KeyError:
                pass

    def remove_subtask_from_db(self, task, subtask):
        if self.db is not None:
            data = self.db[task]
            del data[subtask]
            self.db[task] = data

    def modify_task(self, task: object):
        # TODO
        pass

    def modify_subtask(self, subtask: object):
        # TODO
        pass


if __name__ == '__main__':
    D = DBConnectionShelve()
    D.connect("../data/db")
    D.add_task_to_db("test task3")
    D.add_task_to_db("second task3")
    for k, v in D.db.items():
        print(k, v)
