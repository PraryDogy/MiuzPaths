import os
import string
import threading
from difflib import SequenceMatcher
from typing import Literal

from cfg import cnf

from .pre_paths import PrePaths

__all__ = ("PathFinder", )


class Task:
    t: threading.Thread = None


class PathFinderResult:
    r = None


class SimilarityPercentage(float):
    def __new__(cls, str1: str, str2: str) -> 'SimilarityPercentage':
        return float.__new__(cls, cls.calculate(str1, str2))

    @staticmethod
    def calculate(str1: str, str2: str) -> float:
        matcher = SequenceMatcher(None, str1, str2).ratio()
        return round(matcher * 100, 2)
    

class PathFinderBasePath(object):
    def __init__(self, src_path: str) -> Literal["converted path for mac"]:
        pre_paths = [self.normalize_path(path=i)
                    for i in PrePaths().pre_paths]

        src_path = self.normalize_path(path=src_path)
        src_path_split = [i for i in src_path.split(os.sep) if i]

        self.src_path_versions = [
            os.path.join(pre_path, *src_path_split[i:])
            for pre_path in pre_paths
            for i in range(len(src_path_split))
            ]

        for path_ver in self.src_path_versions:
            if os.path.exists(path_ver):
                self.path = path_ver
                break

    def normalize_path(self, path: Literal["path"]) -> Literal["path without trash"]:
        path = path.replace("\\", os.sep).strip().strip(os.sep)
        path = [i for i in path.split(os.sep) if i]
        return os.path.join(os.sep, *path)


class NearlyPath(PathFinderBasePath):
    def __init__(self, src_path: str):
        PathFinderBasePath.__init__(self, src_path=src_path)

        if hasattr(self, "path"):
            return

        new_paths_versions = []
        for path_ver in self.src_path_versions:
            path_ver_split = [i for i in path_ver.split(os.sep) if i]

            for i in reversed(range(len(path_ver_split))):
                try:
                    new_paths_versions.append(
                        os.path.join(os.sep, *path_ver_split[:i]))
                except TypeError:
                    pass

        new_paths_versions = [i for i in new_paths_versions if len(i) > 1]
        new_paths_versions.sort(key=len, reverse=True)

        for i in new_paths_versions:
            if os.path.exists(i):
                self.path = self.nearly_path = i
                break


class MistakeFinder(NearlyPath):
    def __init__(self, src_path: str):
        NearlyPath.__init__(self, src_path=src_path)

        if not hasattr(self, "nearly_path"):
            return
        
        mistaked_tail = self.find_tail(
            src_path=src_path, nearly_path=self.nearly_path)
        

        for i in mistaked_tail:
            true_name = self.find_true_name(
                path_chunk=i, nearly_path=self.nearly_path)
            if true_name:
                self.nearly_path = os.path.join(self.nearly_path, true_name)
                continue
            else:
                break

        self.path = self.nearly_path

    def find_tail(self, src_path: str, nearly_path: str) -> tuple:
        for i in range(len(nearly_path)):
            if nearly_path[i:] in src_path:
                mistaked_tail = src_path.split(nearly_path[i:])[-1]
                mistaked_tail = self.normalize_path(path=mistaked_tail)
                return [i for i in mistaked_tail.split(os.sep) if i]

    def find_true_name(self, path_chunk: str, nearly_path: str):
        for i in os.listdir(nearly_path):
            if SimilarityPercentage(i, path_chunk) > 90:
                return i

    def similar(self, a: str, b: str):
        return SequenceMatcher(None, a, b).ratio()
        
    def normalize_name(self, name: str) -> Literal["str with letters and digits only"]:
        name, ext = os.path.splitext(p=name)
        name = name.translate(str.maketrans("", "", string.punctuation + " "))
        return f"{name}{ext}"


class PathFinderBase(MistakeFinder):
    def __init__(self, path: str):
        MistakeFinder.__init__(self, src_path=path)
        PathFinderResult.r = self.path


class PathFinder:
    def __init__(self, path: str):
        try:
            while Task.t.is_alive():
                cnf.root.update()
        except AttributeError:
            pass

        Task.t = threading.Thread(target=PathFinderBase, args=[path], daemon=True)
        Task.t.start()

        while Task.t.is_alive():
            cnf.root.update()

    def __str__(self) -> str:
        return PathFinderResult.r



path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "/Users/Morkowik/Downloads/Геохимия видео"
path = "smb://sbc01/shares/Marketing/Photo/_Collections/1 Solo/1 IMG/2023-09-22 11-27-28 рабочий файл.tif/"
path = "smb://sbc031/shares/Marketing/Photo/_Collections/_____1 Solo/1 IMG/__2023-09-22 11-27-28 рабочий файл.tif/"
path = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\)2023\\7. PR-рассылка\\10. Октябрь\\Royal"
path = "fafdgfagrf"

