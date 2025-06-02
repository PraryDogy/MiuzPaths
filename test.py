src = "asdgfsdfasdfsd"

# существующий путь
src = "/Volumes/Shares/Studio/MIUZ/Photo/Art/Ready/000 Лукас/2 Model IMG/LU6057.psd"


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
a.get_result()

print(a.result)