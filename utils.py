import os
import re
import threading
import tkinter
import traceback


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
    

class _Task:
    current: threading.Thread = None

    volumes_dir: str = "/Volumes"
    users_dir: str = "/Users"

    def __init__(self, main_item: MainItem, input_path: str):
        super().__init__()
        self.main_item = main_item
        self.input_path = input_path
        self.result: str | None = None

        self.volumes_list: list[str] = self.get_volumes()
        self.macintosh_hd = self.get_sys_volume()
        self.volumes_list.remove(self.macintosh_hd)

        # /Volumes/Macintosh HD/Volumes
        self.invalid_volume_path: str = self.macintosh_hd + _Task.volumes_dir

    def get_result(self) -> str | None:
        self.prepare_path()

        if self.is_local_path():
            self.result = self.input_path
            return self.result

        paths = self.add_to_start(self.path_to_list(self.input_path))
        paths.sort(key=len, reverse=True)
        result = self.check_for_exists(paths)

        if not result:
            paths = [
                p
                for base in paths
                for p in self.del_from_end(base)
            ]
            paths.sort(key=len, reverse=True)
            result = self.check_for_exists(paths)

        self.result = result or self.main_item.error_text

        return self.result
    
    def is_local_path(self):
        if self.input_path.startswith((_Task.users_dir, self.macintosh_hd)):
            return True
        return False

    def check_for_exists(self, paths: list[str]) -> str | None:
        for path in paths:
            if not os.path.exists(path):
                continue
            if path in self.volumes_list or path == self.invalid_volume_path:
                continue
            return path
        return None
            
    def get_volumes(self) -> list[str]:
        return [
            entry.path
            for entry in os.scandir(_Task.volumes_dir)
            if entry.is_dir()
        ]
    
    def get_sys_volume(self):
        user = os.path.expanduser("~")
        app_support = f"{user}/Library/Application Support"

        for i in self.volumes_list:
            full_path = f"{i}{app_support}"
            if os.path.exists(full_path):
                return i
        return None

    def prepare_path(self):
        path = self.input_path.strip().strip("'\"")
        path = path.replace("\\", "/")
        path = path.strip("/")
        self.input_path = "/" + path

    def path_to_list(self, path: str) -> list[str]:
        return [
            i
            for i in path.split(os.sep)
            if i
        ]

    def add_to_start(self, splited_path: list) -> list[str]:
        """
        Пример:
        >>> splited_path = ["Volumes", "Shares-1", "Studio", "MIUZ", "Photo", "Art", "Raw", "2025"]
        [
            '/Volumes/Shares/Studio/MIUZ/Photo/Art/Raw/2025',
            '/Volumes/Shares/MIUZ/Photo/Art/Raw/2025',
            '/Volumes/Shares/Photo/Art/Raw/2025',
            '/Volumes/Shares/Art/Raw/2025',
            '/Volumes/Shares/Raw/2025',
            '/Volumes/Shares/2025',
            ...
            '/Volumes/Shares-1/Studio/MIUZ/Photo/Art/Raw/2025',
            '/Volumes/Shares-1/MIUZ/Photo/Art/Raw/2025',
            '/Volumes/Shares-1/Photo/Art/Raw/2025',
            ...
        ]
        """
        new_paths = []

        for vol in self.volumes_list:

            splited_path_copy = splited_path.copy()
            while len(splited_path_copy) > 0:

                new = vol + os.sep + os.path.join(*splited_path_copy)
                new_paths.append(new)
                splited_path_copy.pop(0)

        return new_paths
        
    def del_from_end(self, path: str) -> list[str]:
        """
        Пример:
        >>> path: "/sbc01/Shares/Studio/MIUZ/Photo/Art/Raw/2025"
        [
            "/sbc01/Shares/Studio/MIUZ/Photo/Art/Raw/2025",
            "/sbc01/Shares/Studio/MIUZ/Photo/Art/Raw",
            "/sbc01/Shares/Studio/MIUZ/Photo/Art",
            "/sbc01/Shares/Studio/MIUZ/Photo",
            "/sbc01/Shares/Studio/MIUZ",
            "/sbc01/Shares/Studio",
            "/sbc01/Shares",
            "/sbc01",
        ]
        """
        new_paths = []

        while path != os.sep:
            new_paths.append(path)
            path, _ = os.path.split(path)

        return new_paths
    

class PathFinder:
    def __init__(self, path: str, root: tkinter.Tk, main_item: MainItem):
        try:
            while _Task.current.is_alive():
                root.update()
        except AttributeError:
            pass
        
        self.main_item = main_item
        self.root = root
        self.input_path = path

        self.task_ = _Task(self.main_item, path)

        target = self.task_.get_result
        _Task.current = threading.Thread(target=target)
        _Task.current.start()

        while _Task.current.is_alive():
            root.update()

    def get_result(self) -> str:
        return self.task_.result



path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "/Users/Morkowik/Downloads/Геохимия видео"
path = "smb://sbc01/shares/Marketing/Photo/_Collections/1 Solo/1 IMG/2023-09-22 11-27-28 рабочий файл.tif/"
path = "smb://sbc031/shares/Marketing/Photo/_Collections/_____1 Solo/1 IMG/__2023-09-22 11-27-28 рабочий файл.tif/"
path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\)2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "fafdgfagrf"
"/Volumes/Shares/Marketing/Design/PROMO_АКЦИИ/2025/03_Spring Gifts/_8 march_Video/AI pix/Rich out.psd"
"/Volumes/Shares/Studio/MIUZ/Photo/Art/FOR RETOUCHERS/Retouch Comments"