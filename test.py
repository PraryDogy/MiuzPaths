src = "asdgfsdfasdfsd"

# существующий путь
src = "/Volumes/Shares-1/Studio/MIUZ/Photo/Art/Ready/000 Лукас/2 Model IMG/LU6057.psd"
src = '/Users/Loshkaredfdfdv/Desktop/2024-01-26 10-47-24.tif'
src = '/Volumes/Macintosh HD/Users/Loshkarev11/Desktop/2024-01-26 10-47-24.tif'
src = "\MIUZ\Video\Digital\Ready\2025\6. Июнь"

from path_finder import PathFinder

a = PathFinder(src)
a._get_volumes()
b = a._get_deep_level()

print(a._volumes_list)