import tkinter
from tkinter import Menu, Event
from cfg import cnf

class ContextMenu(Menu):
    def __init__(self, e: Event):
        Menu.__init__(self, master=cnf.root)

        self.add_command(label="Очистить",
                         command=lambda: self.clear(e=e))
        self.add_separator()
        self.add_command(label="Очистить все",
                         command=lambda: self.clear_all(e=e))

    def clear(self, e: Event = None):
        print("clear current path")
        e.widget.destroy()

    def clear_all(self, e: Event = None):
        print("clear all paths")
