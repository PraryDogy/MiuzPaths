"\192.168.10.105\Shares\Marketing\External\Фото_и_видео_Магазинов"
"\sbc01\Shares\Marketing\General\4. MONTHLY TO START\МАРТ\ADV& PR\ФОТО"
"\Marketing\Photo\2022\05 - май\Миллениум_предметка\R01-MLN119-070-_-2022-05-17 22-09-08"
"\192.168.10.105\Shares\Google Drive\Loshkarev\Book"
"Z:\Marketing\Photo\2022\05 - май\Миллениум_предметка\R01-MLN119-070-_-2022-05-17 22-09-08"
"smb:/192.168.10.105/Shares/Marketing/Photo/2022/05 - май/Срочные браслеты Шмаи/Retouch"
"/Volumes/Shares/Google Drive/Loshkarev/Book"
"/Users/evlosh/Downloads/AutopanoGiga3.5.dmg"
"marketing\Photo\2022\05 - май\Миллениум_предметка\R01-MLN119-070-_-2022-05-17 22-09-08"
"\sbc01\shares\marketing\General\4. MONTHLY TO START\МАРТ\ADV& PR\ФОТО"
"/Marketing/Photo/2022/05 - май/Срочные браслеты Шмаи/Retouch"


from difflib import SequenceMatcher

class SimilarityPercentage(float):
    def __new__(cls, str1: str, str2: str) -> 'SimilarityPercentage':
        return float.__new__(cls, cls.calculate(str1, str2))

    @staticmethod
    def calculate(str1: str, str2: str) -> float:
        matcher = SequenceMatcher(None, str1, str2).ratio()
        return round(matcher * 100, 2)

# Пример использования
string1 = "6. PR-рассылка"
string2 = "7. PR-рассылка"

percentage = SimilarityPercentage(string1, string2)
if percentage > 90:
    print(percentage)