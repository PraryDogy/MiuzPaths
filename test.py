import os

user_path = '/Users/Morkowik/Downloads/Файлы (1).zip'
path2 = '/Users/Morkowik/Desktop/Evgeny/MiuzPaths/venv/bin/activate'
bad_path = '/Users/Morkowik/Desktopp/Evgeny/MiuzPaths/venv/bin/activate'


def remove_file(input):
    if os.path.isfile(input):
        return os.path.split(input)[0]
    return input


print(remove_file('iuzPaths Loshk'))



# /Volumes/Shares/Marketing/Externa/Фото_и_видео_Магазинов/Фото_магазинов


