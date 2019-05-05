"""
    Controller fo communication with model
"""


class TaskListController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def get_tasks(self):
        tasks = self.model.tasks.items_sorted
        return tasks

    def get_subtasks(self):
        if self.model.tasks.active_task is not None:
            subtasks = self.model.tasks.active_task.subtasks.items_sorted
            return subtasks

    def create_new_task(self, description):
        self.model.add_task_to_db(description)

    def create_new_subtask(self, description):
        self.model.add_subtask_to_db(self.model.tasks.active_task, description)

    def modify_task(self, primary_k, **kwargs):
        self.model.modify_task_in_db(primary_k, **kwargs)

    def modify_subtask(self, primary_k, subtask_primary, **kwargs):
        self.model.modify_subtask_in_db(primary_k, subtask_primary, **kwargs)

    def toggle_completed(self, item_type:str):
        if item_type == "subtask" or item_type == "both":
            self.modify_subtask(self.model.tasks.active_task.description,
                                self.model.tasks.active_task.subtasks.active_subtask.description,
                                completed=not self.model.tasks.active_task.subtasks.active_subtask.completed)
        elif item_type == "task" or item_type == "both":
            self.modify_task(self.model.tasks.active_task.description,
                             completed=self.is_task_completed(self.model.tasks.active_task))

    @staticmethod
    def is_task_completed(task):
        if len(task.subtasks.items) == 0:
            return False
        for subtask in task.subtasks.items.values():
            if not subtask.completed:
                return False
        return True

    def remove_task(self):
        seq = self.model.tasks.active_task.sequence
        tasks_count = len(self.get_tasks())
        description = self.model.tasks.active_task.description
        if tasks_count > 1:
            if seq == tasks_count:
                task_to_select = seq - 2
            else:
                task_to_select = seq
            self.select_item("task", task_to_select)
        else:
            self.model.tasks.active_task = None
        self.model.remove_task_from_db(description)

    def remove_subtask(self):
        seq = self.model.tasks.active_task.subtasks.active_subtask.sequence
        subtasks_count = len(self.get_subtasks())
        description = self.model.tasks.active_task.subtasks.active_subtask.description
        if subtasks_count > 1:
            if seq == subtasks_count:
                subtask_to_select = seq - 2
            else:
                subtask_to_select = seq
            self.select_item("subtask", subtask_to_select)
        else:
            self.model.tasks.active_task.subtasks.active_subtask = None
        self.model.remove_subtask_from_db(self.model.tasks.active_task.description,
                                          description)

    def go_up(self, list_type: str):
        if list_type == "task":
            seq = self.model.tasks.active_task.sequence
            if seq > 1:
                self.select_item(list_type, seq-2)
        elif list_type == "subtask":
            seq = self.model.tasks.active_task.subtasks.active_subtask.sequence
            if seq > 1:
                self.select_item(list_type, seq-2)

    def go_down(self, list_type: str):
        if list_type == "task":
            seq = self.model.tasks.active_task.sequence
            if seq < len(self.model.tasks):
                self.select_item(list_type, seq)
        elif list_type == "subtask":
            seq = self.model.tasks.active_task.subtasks.active_subtask.sequence
            if seq < len(self.model.tasks.active_task.subtasks):
                self.select_item(list_type, seq)

    def select_item(self, list_type: str, sequence: int=None):
        if list_type == "task":
            if self.model.tasks.active_task:
                self.model.modify_task_in_db(self.model.tasks.active_task.description, selected=False)
            if sequence is not None:
                new_item = self.model.tasks.items_sorted[sequence]
                self.model.modify_task_in_db(new_item.description, selected=True)
                self.model.tasks.active_task = self.model.tasks.items_sorted[sequence]
            else:
                self.model.tasks.active_task = None
        elif list_type == "subtask":
            if self.model.tasks.active_task.subtasks.active_subtask:
                self.model.modify_subtask_in_db(self.model.tasks.active_task.description,
                                                self.model.tasks.active_task.subtasks.active_subtask.description,
                                                selected=False)
            if sequence is not None:
                new_item = self.model.tasks.active_task.subtasks.items_sorted[sequence]
                self.model.modify_subtask_in_db(self.model.tasks.active_task.description,
                                                new_item.description,
                                                selected=True)
                self.model.tasks.active_task.subtasks.active_subtask = self.model.tasks.active_task.subtasks.items_sorted[sequence]
            else:
                self.model.tasks.active_task.subtasks.active_subtask = None

    def validate_task(self, description):
        return self.model.validate_task(description)

    def validate_subtask(self, description):
        return self.model.validate_subtask(description)

    def get_selected_subtask(self):
        return self.model.tasks.active_task.subtasks.active_subtask

    def get_selected_task(self):
        return self.model.tasks.active_task
