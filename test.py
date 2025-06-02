src = "asdgfsdfasdfsd"


from utils import _Task, MainItem


class MainItem:
    def __init__(self):
        self.path_list: list[str] = []
        self.none_type: str = "None"
        self.error_text: str = "\n".join([
            "Не могу найти путь к файлу/папке",
            "Скопируйте путь в буфер обмена",
            "Подключите сетевой диск"
        ])


main_item = MainItem()
a = _Task(main_item, src)
res = a.get_result()