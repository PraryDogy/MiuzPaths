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
    

class PathFinderTask:
    current_task: threading.Thread = None
    result: str = None
    volumes: list[str] = None
    volumes_text: str = "/Volumes"
    users: str = "/Users"
    inner_volumes: str = None

    def __init__(self, main_item: MainItem):
        super().__init__()
        self.main_item = main_item

    def get_result(self, path: str) -> str | None:
        PathFinderTask.volumes = self.get_volumes()
        sys_volume = self.get_sys_volume(PathFinderTask.volumes)
        PathFinderTask.inner_volumes = sys_volume + PathFinderTask.volumes_text

        # удаляем новые строки, лишние слешы
        _prepared = self.prepare_path(path)

        if _prepared.startswith(PathFinderTask.users):
            _prepared = sys_volume + _prepared


        # if prepared is None or prepared.count(os.sep) == 1:
        #     PathFinderTask.result = self.main_item.error_text
        #     return

        # elif os.path.exists(prepared):
        #     PathFinderTask.result = prepared
        #     return
        
        # else:
        #     PathFinderTask.result = prepared

        # превращаем путь в список 
        splited = self.path_to_list(_prepared)

        # см. аннотацию add_to_start
        paths = self.add_to_start(splited, PathFinderTask.volumes)
        res = self.check_for_exists(paths)

        if res in (*PathFinderTask.volumes, PathFinderTask.inner_volumes):
            PathFinderTask.result = self.main_item.error_text

        elif res:
            PathFinderTask.result = res
        
        elif res is None:
            # см. аннотацию метода del_from_end
            paths = [
                ended_path
                for path_ in paths
                for ended_path in self.del_from_end(path_)
            ]

            paths.sort(key=len, reverse=True)
            res = self.check_for_exists(paths)

            if res in (*PathFinderTask.volumes, PathFinderTask.inner_volumes) or res is None:
                PathFinderTask.result = self.main_item.error_text
            else:
                PathFinderTask.result = res
            

    def get_volumes(self) -> list[str]:
        return [
            entry.path
            for entry in os.scandir(PathFinderTask.volumes_text)
            if entry.is_dir()
        ]
    
    def get_sys_volume(self, volumes: list[str]):
        user = os.path.expanduser("~")
        app_support = f"{user}/Library/Application Support"

        for i in volumes:
            full_path = f"{i}{app_support}"
            if os.path.exists(full_path):
                return i
        return None

    def prepare_path(self, path: str) -> str:
        path = path.replace("\\", os.sep)
        path = path.strip()
        path = path.strip("'").strip('"') # кавычки
        if path:
            return os.sep + path.strip(os.sep)
        else:
            return None

    def path_to_list(self, path: str) -> list[str]:
        return [
            i
            for i in path.split(os.sep)
            if i
        ]

    def add_to_start(self, splited_path: list, volumes: list[str]) -> list[str]:
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
    
    def check_for_exists(self, paths: list[str]) -> str | None:
        for i in paths:
            if os.path.exists(i):
                return i
        return None
    
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
            while PathFinderTask.current_task.is_alive():
                root.update()
        except AttributeError:
            pass
        
        self.main_item = main_item
        self.task_ = PathFinderTask(self.main_item)
        PathFinderTask.current_task = threading.Thread(
            target=self.task_.get_result,
            args=[path],
            daemon=True
        )

        PathFinderTask.current_task.start()

        while PathFinderTask.current_task.is_alive():
            root.update()

    def get_result(self) -> str:
        return PathFinderTask.result



path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "/Users/Morkowik/Downloads/Геохимия видео"
path = "smb://sbc01/shares/Marketing/Photo/_Collections/1 Solo/1 IMG/2023-09-22 11-27-28 рабочий файл.tif/"
path = "smb://sbc031/shares/Marketing/Photo/_Collections/_____1 Solo/1 IMG/__2023-09-22 11-27-28 рабочий файл.tif/"
path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\)2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "fafdgfagrf"
"/Volumes/Shares/Marketing/Design/PROMO_АКЦИИ/2025/03_Spring Gifts/_8 march_Video/AI pix/Rich out.psd"
"/Volumes/Shares/Studio/MIUZ/Photo/Art/FOR RETOUCHERS/Retouch Comments"