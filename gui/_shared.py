import tkinter


class _Shared:
    string_var = tkinter.StringVar()
    path_list: list[str] = []
    none_type: str = "None"
    error_text: str = "\n".join([
        "Не могу найти путь к файлу/папке",
        "Скопируйте путь в буфер обмена",
        "Подключите сетевой диск"
    ])