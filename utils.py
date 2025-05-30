import os
import re
import threading
import tkinter
import traceback

from cfg import cnf


class Shared:
    string_var = tkinter.StringVar()
    path_list: list[str] = []
    none_type: str = "None"
    error_text: str = "\n".join([
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
    

class Task:
    current_task: threading.Thread = None
    result: str = "Скопируйте путь в буфер обмена"
    volumes: list = None
    volumes_text = "/Volumes"

    @classmethod
    def get_result(cls, path: str) -> str | None:        
        Task.volumes = cls.get_volumes()
        sys_volume = cls.get_sys_volume(Task.volumes)
        if sys_volume and sys_volume in Task.volumes:
            Task.volumes.remove(sys_volume)

        # удаляем новые строки, лишние слешы
        prepared = cls.prepare_path(path)

        if not prepared:
            Task.result = Shared.error_text
            return None

        elif os.path.exists(prepared):
            Task.result = prepared
            return prepared

        # превращаем путь в список 
        splited = cls.path_to_list(path=prepared)

        # см. аннотацию add_to_start
        paths = cls.add_to_start(splited_path=splited, volumes=Task.volumes)

        res = cls.check_for_exists(paths=paths)

        if res in Task.volumes:
            Task.result = Shared.error_text
            return None

        elif res:
            Task.result = res
            return res
        
        else:
            # см. аннотацию метода del_from_end
            paths = [
                ended_path
                for path_ in paths
                for ended_path in cls.del_from_end(path=path_)
            ]

            paths.sort(key=len, reverse=True)
            
            res = cls.check_for_exists(paths=paths)

            if res in Task.volumes:
                Task.result = Shared.error_text
                return None
            
            elif res:
                Task.result = res
                return res

    @classmethod
    def is_path(cls, s: str) -> bool:
        s = s.replace("\\", "/")
        pattern = r'^(/[^/\0]+)+/?$'
        return bool(re.match(pattern, s))

    @classmethod
    def get_volumes(cls) -> list[str]:
        return [
            entry.path
            for entry in os.scandir(cls.volumes_text)
            if entry.is_dir()
        ]
    
    @classmethod
    def get_sys_volume(cls, volumes: list[str]):
        user = os.path.expanduser("~")
        app_support = f"{user}/Library/Application Support"

        for i in volumes:
            full_path = f"{i}{app_support}"
            if os.path.exists(full_path):
                return i
        return None

    @classmethod
    def prepare_path(cls, path: str) -> str:
        path = path.replace("\\", os.sep)
        path = path.strip()
        path = path.strip("'").strip('"') # кавычки
        if path:
            return os.sep + path.strip(os.sep)
        else:
            return None

    @classmethod
    def path_to_list(cls, path: str) -> list[str]:
        return [
            i
            for i in path.split(os.sep)
            if i
        ]

    @classmethod
    def add_to_start(cls, splited_path: list, volumes: list[str]) -> list[str]:
        """
        Пример:
        >>> splited_path = ["Volumes", "Shares-1", "Studio", "MIUZ", "Photo", "Art", "Raw", "2025"]
        >>> volumes = ["/Volumes/Shares", "/Volumes/Shares-1"]
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

        for vol in volumes:

            splited_path_copy = splited_path.copy()
            while len(splited_path_copy) > 0:

                new = vol + os.sep + os.path.join(*splited_path_copy)
                new_paths.append(new)
                splited_path_copy.pop(0)

        new_paths.sort(key=len, reverse=True)
        return new_paths
    
    @classmethod
    def check_for_exists(cls, paths: list[str]) -> str | None:
        for i in paths:
            if os.path.exists(i):
                return i
        return None
    
    @classmethod
    def del_from_end(cls, path: str) -> list[str]:
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
    def __init__(self, path: str):
        try:
            while Task.current_task.is_alive():
                cnf.root.update()
        except AttributeError:
            pass

        Task.current_task = threading.Thread(
            target=Task.get_result,
            args=[path],
            daemon=True
        )

        Task.current_task.start()

        while Task.current_task.is_alive():
            cnf.root.update()

    def get_result(self) -> str:
        return Task.result



path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "/Users/Morkowik/Downloads/Геохимия видео"
path = "smb://sbc01/shares/Marketing/Photo/_Collections/1 Solo/1 IMG/2023-09-22 11-27-28 рабочий файл.tif/"
path = "smb://sbc031/shares/Marketing/Photo/_Collections/_____1 Solo/1 IMG/__2023-09-22 11-27-28 рабочий файл.tif/"
path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\)2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "fafdgfagrf"
"/Volumes/Shares/Marketing/Design/PROMO_АКЦИИ/2025/03_Spring Gifts/_8 march_Video/AI pix/Rich out.psd"
"/Volumes/Shares/Studio/MIUZ/Photo/Art/FOR RETOUCHERS/Retouch Comments"