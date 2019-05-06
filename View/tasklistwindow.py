"""
    Representing a particular window on scren
"""
from View.Observer import Observer, Observable
from curses import echo, noecho, curs_set, A_REVERSE, A_UNDERLINE, color_pair
from curses.textpad import Textbox


class TaskListWindow(Observer, Observable):

    def __init__(self, name, window, view, controller):
        Observable.__init__(self)
        self.name = name
        self.active_item_name = ""
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
                completed = "v" if item.completed else "x"
                if item.is_selected:
                    style = A_REVERSE
                if item.completed:
                    style = style | color_pair(10)
                text = "%s %s. %s" % (completed, item.sequence, item.description)
                maxx = self.window.getmaxyx()[1]
                text = (text[:maxx - 6] + "...") if len(text) > maxx - 3 else text
                self.window.addstr(idx+1, 1, "{text: <{width}}".format(text=text, width=self.window.getmaxyx()[1]-2), style)

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
            266: ("F2", "Modify", self.modify_task),
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

    def modify_task(self):
        current_task = self.controller.get_selected_task()
        curs_set(2)
        try:
            from math import ceil
            max_rows = ceil(len(current_task.description) / (self.window.getmaxyx()[1] - 2))

            # Display hint
            self.view.command_window.display_text("Ctrl+G - Save Result")

            edit_win = self.window.subwin(max_rows, self.window.getmaxyx()[1] - 2, current_task.sequence+3, 1)
            edit_win.clear()
            edit_win.addstr(0, 0, self.controller.get_selected_task().description)
            edit_win.move(0, 0)
            e = Textbox(edit_win, insert_mode=True)
            text = self.controller.sanitize_input(e.edit())
            self.controller.modify_task(self.controller.get_selected_task().description, description=text)
        finally:
            curs_set(0)
            self.render(self.controller.get_tasks())
            self.notify()

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
        self.controller.toggle_completed("task")
        self.render(self.controller.get_tasks())


class SubtasksWindow(TaskListWindow):

    def __init__(self, name, window, view, controller):
        super().__init__(name, window, view, controller)
        self.commands = {
            259: ("Up", "Arrow up", self.go_up),  # up arrow key
            258: ("Down", "Arrow down", self.go_down),  # down arrow key
            330: ("Delete", "Delete task", self.remove_subtask),
            266: ("F2", "Modify", self.modify_subtask),
            267: ("F3", "Add new", self.add_subtask),
            268: ("F4", "Toggle completed", self.set_completed),
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
            self.notify()

    def modify_subtask(self):
        current_subtask = self.controller.get_selected_subtask()
        curs_set(2)
        try:
            from math import ceil
            max_rows = ceil(len(current_subtask.description) / (self.window.getmaxyx()[1] - 2))

            # Display hint
            self.view.command_window.display_text("Ctrl+G - Save Result")

            edit_win = self.window.subwin(max_rows, self.window.getmaxyx()[1] - 2,
                                          current_subtask.sequence+3, self.view.tasks_window.window.getmaxyx()[1]+2)
            edit_win.clear()
            edit_win.addstr(0, 0, self.controller.get_selected_subtask().description)
            edit_win.move(0, 0)
            e = Textbox(edit_win, insert_mode=True)
            text = self.controller.sanitize_input(e.edit())
            self.controller.modify_subtask(self.controller.get_selected_task().description,
                                           self.controller.get_selected_subtask().description,
                                           description=text)
        finally:
            curs_set(0)
            self.render(self.controller.get_subtasks())
            self.notify()

    def set_completed(self):
        self.controller.toggle_completed("both")
        self.render(self.controller.get_subtasks())
        self.notify()

    def focus_next_window(self):
        self.controller.select_item("subtask")
        super().focus_next_window()
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

    def display_text(self, text):
        self.window.clear()
        self.window.border()
        self.view.print_center(1, text, self.window)
        self.window.refresh()

    def update(self):
        self.render(self.view.active_window.commands)
