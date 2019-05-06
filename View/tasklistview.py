"""
    This file will present the tasks and subtasks on the screen.
    This one particularly will use curses, but can be rewritten to use something else (ex. Tkinter)
"""
import curses
import os, sys, locale

sys.path.append(os.path.abspath(".."))

from Model.tasklistmodel import TaskListModel
from Model.dbconfig import DBConnectionShelve
from Controller.tasklistcontroller import TaskListController
from View.tasklistwindow import TasksWindow, SubtasksWindow, CommandsWindow

locale.setlocale(locale.LC_ALL, '')

class TaskListView:

    def __init__(self, model, controller=None):
        self.model = model
        self.controller = controller
        self.tasks_window = None
        self.subtasks_window = None
        self.command_window = None
        self.active_window = None
        self.focusable_windows = []

    def init_screen(self):

        def main(stdscr):
            # Set the terminal full screen
            curses.curs_set(0)
            curses.init_pair(10, curses.COLOR_GREEN, 0)
            curses.init_pair(11, 0, curses.COLOR_RED)
            # curses.resize_term(30, 160)
            win = curses.newwin(3, curses.COLS - 2, 0, 0)
            tasks_width = int(stdscr.getmaxyx()[1] * 0.4)   # get task list width of 40%
            self.tasks_window = TasksWindow("Tasks", curses.newwin(curses.LINES - 7, tasks_width, 3, 0), self, self.controller)
            self.set_active_window(self.tasks_window)
            self.tasks_window.window.keypad(True)
            self.subtasks_window = SubtasksWindow("Subtasks", curses.newwin(curses.LINES - 7, curses.COLS-tasks_width-3, 3, tasks_width+1), self, self.controller)
            self.subtasks_window.window.keypad(True)
            self.command_window = CommandsWindow("Commands", curses.newwin(3, curses.COLS - 2, curses.LINES - 4, 0), self, self.controller)
            self.command_window.render(self.active_window.commands)
            self.focusable_windows = [self.tasks_window, self.subtasks_window]
            # register observers
            self.tasks_window.add(self.subtasks_window, self.command_window)
            self.subtasks_window.add(self.tasks_window, self.command_window)
            # get data from Model via controller
            self.refresh_screen()
            while True:

                win.clear()
                win.border()
                self.print_center(1, "Tasker (%s)" % self.active_window.active_item_name, win)
                win.refresh()
                self.tasks_window.window.refresh()
                self.subtasks_window.window.refresh()
                self.command_window.window.refresh()

                k = self.active_window.window.getch()
                if k == 113:
                    break
                else:
                    self.active_window.execute_command(k)
            return True

        if not curses.wrapper(main):
            self.init_screen()

    @staticmethod
    def print_center(line, text, window):
        text = (text[:curses.COLS-8] + "...") if len(text) > curses.COLS-5 else text
        window.addstr(line, curses.COLS//2-len(text)//2, text)

    def refresh_screen(self):
        self.tasks_window.render(self.controller.get_tasks())
        self.subtasks_window.render(self.controller.get_subtasks())

    def set_controller(self, controller):
        self.controller = controller

    def set_active_window(self, win):
        self.active_window = win
        if isinstance(win, TasksWindow):
            self.active_window.active_item_name = self.controller.get_selected_task().description

    def focus_next_window(self):
        for idx, win in enumerate(self.focusable_windows):
            if id(self.active_window) == id(win):
                self.active_window = self.focusable_windows[(idx + 1) % len(self.focusable_windows)]
                self.active_window.notify()
                return


if __name__ == '__main__':
    model = TaskListModel(DBConnectionShelve(), "../data/db")
    view = TaskListView(model)
    controller = TaskListController(model, view)
    view.set_controller(controller)
    view.init_screen()