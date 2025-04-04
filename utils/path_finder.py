import os
import threading
from cfg import cnf

__all__ = ("PathFinder", "Shared")


class Shared:
    result_none = "RESULT_NONE"
    path_finder_task: threading.Thread = None
    result: str = None
    volumes: list = None


class PathFinderTask:
    VOLUMES = os.sep + "Volumes"
    EXTRA_PATHS = []

    @classmethod
    def get_result(cls, path: str) -> str | None:

        # игнорируем /Volumes/Macintosh HD
        Shared.volumes = cls.get_volumes()[1:]

        # удаляем новые строки, лишние слешы
        prepared = cls.prepare_path(path=path)

        if not prepared:
            Shared.result = Shared.result_none
            return None

        elif os.path.exists(prepared):
            Shared.result = prepared
            return prepared

        # превращаем путь в список 
        splited = cls.path_to_list(path=prepared)

        # см. аннотацию add_to_start
        paths = cls.add_to_start(splited_path=splited, volumes=Shared.volumes)

        res = cls.check_for_exists(paths=paths)

        if res in Shared.volumes:
            Shared.result = Shared.result_none
            return None

        elif res:
            Shared.result = res
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

            if res in Shared.volumes:
                Shared.result = Shared.result_none
                return None
            
            elif res:
                Shared.result = res
                return res

    @classmethod
    def get_volumes(cls) -> list[str]:
        return [
            entry.path
            for entry in os.scandir(cls.VOLUMES)
            if entry.is_dir()
        ]
    
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
            while Shared.path_finder_task.is_alive():
                cnf.root.update()
        except AttributeError:
            pass

        Shared.path_finder_task = threading.Thread(
            target=PathFinderTask.get_result,
            args=[path],
            daemon=True
        )

        Shared.path_finder_task.start()

        while Shared.path_finder_task.is_alive():
            cnf.root.update()

    def get_result(self) -> str:
        return Shared.result



path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "/Users/Morkowik/Downloads/Геохимия видео"
path = "smb://sbc01/shares/Marketing/Photo/_Collections/1 Solo/1 IMG/2023-09-22 11-27-28 рабочий файл.tif/"
path = "smb://sbc031/shares/Marketing/Photo/_Collections/_____1 Solo/1 IMG/__2023-09-22 11-27-28 рабочий файл.tif/"
path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\)2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "fafdgfagrf"


"/Volumes/Shares/Marketing/Design/PROMO_АКЦИИ/2025/03_Spring Gifts/_8 march_Video/AI pix/Rich out.psd"