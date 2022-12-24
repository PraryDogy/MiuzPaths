import os

user_path = '/Users/Morkowik/Downloads/Файлы (1).zip'


def file_path(input):
    if os.path.isfile(input):
        return os.path.split(input)[0]
    return False

def exists_path(input):
    while not os.path.exists(input):
        input = os.path.split(input)[0]
    return input


print(file_path(user_path))