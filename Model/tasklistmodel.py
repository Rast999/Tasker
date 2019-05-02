from Model.dbconfig import DBConnectionShelve
from Model.task import Task, TaskList


class TaskListModel:

    def __init__(self, dbconnectiontype, dbname):
        self.tasks = TaskList()
        self.dbconnectiontype = dbconnectiontype
        self.db = None
        self.connect(dbname)
        self.sync()

    def connect(self, dbname):
        self.db = self.dbconnectiontype.connect(dbname)

    def sync(self):
        self.tasks = self.dbconnectiontype.sync(self.tasks)

    def add_task_to_db(self, description: str) -> None:
        seq = len(self.tasks.items.keys()) + 1
        self.dbconnectiontype.add_task_to_db(description, seq)
        # self.tasks[description] = Task(description)
        self.tasks.add_task(description, sequence=seq)

    def add_subtask_to_db(self, task: object, description: str) -> None:
        seq = len(self.tasks[task.description].subtasks.items.keys())+1
        self.dbconnectiontype.add_subtask_to_db(task, description, seq)
        self.tasks[task.description].subtasks.add_subtask(description, task, sequence=seq)

    def remove_task_from_db(self, primary_key) -> None:
        self.dbconnectiontype.remove_task_from_db(primary_key)
        self.tasks.remove_task(primary_key)

    def remove_subtask_from_db(self, task_primary, subtask_primary):
        self.dbconnectiontype.remove_subtask_from_db(task_primary, subtask_primary)
        self.tasks[task_primary].subtasks.remove_subtask(subtask_primary)

    def modify_task_in_db(self, primary_key: str, description: str = None,
                          completed: bool = None, selected: bool = None) -> None:
        self.dbconnectiontype.modify_task(primary_key, description, completed, selected)
        self.tasks.modify_task(primary_key, description, completed, selected)

    def modify_subtask_in_db(self, primary_k: str, subtask_primary: str,
                             description: str = None, completed: bool = None, selected: bool = None):
        self.dbconnectiontype.modify_subtask(primary_k, subtask_primary, description, completed, selected)
        self.tasks[primary_k].subtasks.modify_subtask(subtask_primary, description, completed, selected)

    def print_shelve_db(self):
        # for testing only
        if isinstance(self.dbconnectiontype, DBConnectionShelve):
            result = ""
            for task in self.db.keys():
                result += task
                result += ": ["
                for subtask in self.db[task].keys():
                    if subtask not in self.dbconnectiontype.ignored_fields:
                        result += "%s[%s - %s], " % (subtask, self.db[task][subtask]["completed"], self.db[task][subtask]["sequence"])
                result += "]\n"
            print(result)
        else:
            raise TypeError("Database connection type is not shelve")


if __name__ == "__main__":
    model = TaskListModel(DBConnectionShelve(), "../data/db")
    model.add_task_to_db("test task 1")
    model.add_task_to_db("test task 23")
    model.add_task_to_db("Unnecessary task")
    model.add_subtask_to_db(model.tasks["test task 1"], "some subtask")
    model.add_subtask_to_db(model.tasks["test task 1"], "some subtask 32")
    model.add_subtask_to_db(model.tasks["Unnecessary task"], "some subtask")
    # model.remove_subtask_from_db("test task 1", "some subtask")
    # model.remove_task_from_db("test task 23")
    # model.remove_task_from_db("Unnecessary task")
    model.modify_task_in_db("test task 1", "test task 23", True)
    # model.modify_subtask_in_db("test task 1", "some subtask", "some subtask updated", True)
    model.print_shelve_db()
    print("finish")