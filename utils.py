import os
import re
import threading
import tkinter
import traceback

from path_finder import PathFinder as PathFinder_


class MainItem:
    def __init__(self):
        self.string_var: tkinter.StringVar = tkinter.StringVar()
        self.path_list: list[str] = []
        self.none_type: str = "None"
        self.error_text: str = "\n".join([
            "Не могу найти путь к файлу/папке",
            "Скопируйте путь в буфер обмена",
            "Подключите сетевой диск"
        ])


class Err:
    @classmethod
    def print_error(cls, error: Exception):
        tb = traceback.extract_tb(error.__traceback__)

        # Попробуем найти первую строчку стека, которая относится к вашему коду.
        for trace in tb:
            filepath = trace.filename
            filename = os.path.basename(filepath)
            
            # Если файл - не стандартный модуль, считаем его основным
            if not filepath.startswith("<") and filename != "site-packages":
                line_number = trace.lineno
                break
        else:
            # Если не нашли, то берем последний вызов
            trace = tb[-1]
            filepath = trace.filename
            filename = os.path.basename(filepath)
            line_number = trace.lineno

        msg = str(error)
        if msg.startswith("[Errno"):
            msg = msg.split("]", 1)[-1].strip()

        print(f"\n{type(error).__name__}: {msg}\n{filepath}:{line_number}\n")
        return msg
    

class PathFinder:
    current: threading.Thread

    def __init__(self, path: str, root: tkinter.Tk, main_item: MainItem):
        try:
            while self.current.is_alive():
                root.update()
        except AttributeError:
            pass
        
        self.main_item = main_item
        self.root = root
        self.input_path = path

    def run(self):
        self.path_finder_ = PathFinder_(self.input_path)
        target = self.path_finder_.get_result
        self.current = threading.Thread(target=target)
        self.current.start()

        while self.current.is_alive():
            self.root.update()

    def get_result(self) -> str:
        return self.path_finder_.result
