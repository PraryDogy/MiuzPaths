import os
import threading
from difflib import SequenceMatcher
from cfg import cnf

__all__ = ("PathFinder", )


class Shared:
    my_thread: threading.Thread = None
    result: str = None
    volumes: list = None


def path_finder(src: str):
    src = os.sep + src.replace("\\", os.sep).strip().strip(os.sep)
    src_splited = [i for i in src.split(os.sep) if i]
    Shared.volumes = [
        os.path.join("/Volumes", i)
        for i in os.listdir("/Volumes")
        if os.path.ismount(os.path.join("/Volumes", i))
        ]

    volumes_extra = [
        os.path.join(volume_path, extra.replace(os.sep, "").strip())
        for extra in cnf.extra_paths
        for volume_path in Shared.volumes
        ]
    
    Shared.volumes.extend(volumes_extra)

    # обрезаем входящий путь каждый раз на 1 секцию с конца
    possible_paths = {
            os.path.join(*src_splited[:i])
            for i in range(len(src_splited) + 1)
            if src_splited[:i]
            }

    # обрезаем каждый путь на 1 секцию с начала и прибавляем элементы из shares
    all_posible_paths = []

    for p_path in sorted(possible_paths, key=len, reverse=True):
        p_path_split = [i for i in p_path.split(os.sep) if i]
        
        for share in Shared.volumes:
            for i in range(len(p_path_split) + 1):

                all_posible_paths.append(
                    os.path.join(share, *p_path_split[i:])
                    )

    # из всех полученных возможных путей ищем самый подходящий существующий путь
    for i in sorted(all_posible_paths, key=len, reverse=True):
        if os.path.exists(i):
            Shared.result = i
            break

    # смотрим совпадает ли последняя секция входящего и полученного пути
    tail = []

    if Shared.result:
        result_tail = Shared.result.split(os.sep)[-1]
        if src_splited[-1] != result_tail:
            try:
                tail = src_splited[src_splited.index(result_tail) + 1:]
            except ValueError:
                return

    # пытаемся найти секции пути, написанные с ошибкой
    for a in tail:
        dirs = [x for x in os.listdir(Shared.result)]

        for b in dirs:
            matcher = SequenceMatcher(None, a, b).ratio()
            if matcher >= 0.85:
                Shared.result = os.path.join(Shared.result, b)
                break


class PathFinder:
    def __init__(self, path: str):
        try:
            while Shared.my_thread.is_alive():
                cnf.root.update()
        except AttributeError:
            pass

        Shared.my_thread = threading.Thread(target=path_finder, args=[path], daemon=True)
        Shared.my_thread.start()

        while Shared.my_thread.is_alive():
            cnf.root.update()

    def get_result(self) -> str:
        if Shared.result in Shared.volumes:
            return "1/2/3" # open_btn.py > row53 > if len(path) <= 3: ...
        return Shared.result



path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "/Users/Morkowik/Downloads/Геохимия видео"
path = "smb://sbc01/shares/Marketing/Photo/_Collections/1 Solo/1 IMG/2023-09-22 11-27-28 рабочий файл.tif/"
path = "smb://sbc031/shares/Marketing/Photo/_Collections/_____1 Solo/1 IMG/__2023-09-22 11-27-28 рабочий файл.tif/"
path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\)2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "fafdgfagrf"

