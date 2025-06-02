src = "/Users/Morkowik/Desktop/photo_2024-07-30 22.00.11 2.jpg"


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
a = _Task(main_item)