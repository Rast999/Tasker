import shelve
import datetime


class DBConnectionShelve:

    def __init__(self):
        self.db = None

    def connect(self, db_name: str):
        self.db = shelve.open(db_name)
        return self.db

    def close_db(self):
        self.db.close()

    def add_task_to_db(self, description: str):
        if self.db is not None:
            self.db[description] = self.db.get(description, [])

    def add_subtask_to_db(self, task: object, description: str):
        if self.db is not None:
            subtask = dict()
            subtask["description"] = description
            subtask["date_created"] = datetime.datetime.now()
            data = self.db[task.description]
            data.append(subtask)
            self.db[task.description] = data

    def remove_task_from_db(self, task: object):
        if self.db is not None:
            try:
                del self.db[task.description]
            except KeyError:
                pass

    def remove_subtask_from_db(self, task: object, subtask: object):
        if self.db is not None:
            for idx, sub in enumerate(self.db[task.description]):
                if sub["description"] == subtask.description:
                    data = self.db[task.description]
                    data.remove(idx)
                    self.db[task.description] = data

    def modify_task(self, task: object):
        pass

    def modify_subtask(self, subtask: object):
        pass


if __name__ == '__main__':
    D = DBConnectionShelve()
    D.connect("../data/db")
    D.add_task_to_db("test task3")
    D.add_task_to_db("second task3")
    for k, v in D.db.items():
        print(k, v)