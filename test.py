import tkinter
from tkinter import Menu, Event

class ContextMenu(Menu):
    def __init__(self, master: tkinter):
        Menu.__init__(master=master)

        self.add_command(label="Очистить", command=self.clear)
        self.add_separator()
        self.add_command(label="Очистить все", command=self.clear_all)

    def clear(self, e: Event = None):
        "clear current path"
        e.widget.cget("text")

    def clear_all(self, e: Event = None):
        "clear all paths"
