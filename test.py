import re


class Test:
    @classmethod
    def is_windows_path(cls, s: str) -> bool:
        s = s.replace("\\", "\\")
        match = re.match(r".*\\.*", s.strip())
        return bool(match)

    @classmethod
    def is_unix_path(cls, s: str) -> bool:
        s = s.replace("\\", "/")
        pattern = r'^(/[^/\0]+)+/?$'
        return bool(re.match(pattern, s))
    


src = "Z:\\Users\\Admin"
# src = "Test some ome"
# src = "/Ysers/ssdf"
# src = "https://miuz.motivity.ru/login"

is_path = Test.is_windows_path(src)
print(is_path)
is_path = Test.is_unix_path(src)
print(is_path)