"""
    Representing a particular window on scren
"""
from View.Observer import Observer, Observable
from curses import echo, noecho, curs_set


class TaskListWindow(Observer, Observable):

    def __init__(self, name, window, view, controller):
        Observable.__init__(self)
        self.name = name
        self.window = window
        self.commands = dict()
        self.view = view
        self.controller = controller

    def focus_next_window(self):
        self.view.focus_next_window()

    def go_up(self, list_type: str):
        self.controller.go_up(list_type)
        if list_type == "task":
            self.render(self.controller.get_tasks())
        elif list_type == "subtask":
            self.render(self.controller.get_subtasks())
        self.notify()

    def go_down(self, list_type: str):
        self.controller.go_down(list_type)
        if list_type == "task":
            self.render(self.controller.get_tasks())
        elif list_type == "subtask":
            self.render(self.controller.get_subtasks())
        self.notify()

    def update(self):
        raise NotImplementedError("Should be implemented in children")

    def render(self, items: list):
        self.window.clear()
        self.window.border()
        if items:
            for idx, item in enumerate(items):
                style = 0
                if item.is_selected:
                    style = 2097152
                text = "%s. %s" % (item.sequence, item.description)
                self.window.addstr(idx+1, 1, "{text: <{width}}".format(text=text, width=self.window.getmaxyx()[1]-2) , style)

    def execute_command(self, key):
        try:
            return self.commands[key][2]()
        except KeyError:
            pass


class TasksWindow(TaskListWindow):

    def __init__(self, name, window, view, controller):
        super().__init__(name, window, view, controller)
        self.window.border()
        self.commands = {
            259: ("Up", "Arrow up", self.go_up),    # up arrow key
            258: ("Down", "Arrow down", self.go_down),          # down arrow key
            267: ("F3", "Add new", self.add_task),
            330: ("Delete", "Delete task", self.remove_task),
            9: ("Tab", "Edit subtasks", self.focus_next_window)
        }

    def go_up(self):
        return super().go_up("task")

    def go_down(self):
        return super().go_down("task")

    def add_task(self):
        tasks_count = len(self.controller.get_tasks()) + 1
        curs_set(2)
        try:
            echo()
            s = self.window.getstr(tasks_count, 1, self.window.getmaxyx()[1] - 5).strip().decode()
            if self.controller.validate_task(s):
                self.controller.create_new_task(s)
                if tasks_count == 1:
                    self.controller.select_item("task", 0)
        finally:
            curs_set(0)
            noecho()
            self.render(self.controller.get_tasks())

    def remove_task(self):
        val = self.controller.remove_task()
        self.render(self.controller.get_tasks())
        self.notify()
        return val

    def focus_next_window(self):
        super().focus_next_window()
        print(self.controller.get_selected_subtask())
        if len(self.controller.get_subtasks()) > 0 and \
           self.controller.get_selected_subtask() is None:
            self.controller.select_item("subtask", 0)
            self.view.subtasks_window.render(self.controller.get_subtasks())

    def update(self):
        pass


class SubtasksWindow(TaskListWindow):

    def __init__(self, name, window, view, controller):
        super().__init__(name, window, view, controller)
        self.commands = {
            259: ("Up", "Arrow up", self.go_up),  # up arrow key
            258: ("Down", "Arrow down", self.go_down),  # down arrow key
             330: ("Delete", "Delete task", self.remove_subtask),\
            267: ("F3", "Add new", self.add_subtask),
            9: ("Tab", "Edit Tasks", self.focus_next_window)
        }

    def add_subtask(self):
        subtasks_count = len(self.controller.get_subtasks()) + 1
        curs_set(2)
        try:
            echo()
            s = self.window.getstr(subtasks_count, 1, self.window.getmaxyx()[1] - 5).strip().decode()
            if self.controller.validate_subtask(s):
                self.controller.create_new_subtask(s)
                if subtasks_count == 1:
                    self.controller.select_item("subtask", 0)
        finally:
            curs_set(0)
            noecho()
            self.render(self.controller.get_subtasks())

    def focus_next_window(self):
        super().focus_next_window()
        self.controller.select_item("subtask")
        self.render(self.controller.get_subtasks())

    def go_up(self):
        return super(SubtasksWindow, self).go_up("subtask")

    def go_down(self):
        return super(SubtasksWindow, self).go_down("subtask")

    def remove_subtask(self):
        val = self.controller.remove_subtask()
        self.render(self.controller.get_subtasks())
        self.notify()
        return val

    def update(self):
        self.render(self.controller.get_subtasks())


class CommandsWindow(TaskListWindow):

    def __init__(self, name, window, view, controller):
        super().__init__(name, window, view, controller)
        self.text = ""
        pass

    def render(self, commands):
        self.window.clear()
        self.window.border()
        text = ""
        for command in commands.values():
            text += "%s - %s | " % (command[0], command[1])
        self.view.print_center(1, text, self.window)

    def update(self):
        self.render(self.view.active_window.commands)
