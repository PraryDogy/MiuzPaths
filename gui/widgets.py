import os

my_path = '/Volumes/Shares/Marketing/Externarl/Фото_и_видео_Магазинов/Фото_магазинов  '
new_path = os.path.normpath(my_path)
while not os.path.exists(new_path):
    new_path = os.path.split(new_path)[0]

print(new_path)