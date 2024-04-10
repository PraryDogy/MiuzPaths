import os
from difflib import SequenceMatcher


def path_finder(src: str):
    src = os.sep + src.replace("\\", os.sep).strip().strip(os.sep)
    src_splited = [i for i in src.split(os.sep) if i]
    src_final: str = None
    shares = ['/Volumes/Shares', '/Volumes/Shares-1']

    # обрезаем входящий путь каждый раз на 1 секцию с конца
    possible_paths = {
            os.path.join(*src_splited[:i])
            for i in range(len(src_splited) + 1)
            if src_splited[:i]
            }


    # обрезаем каждый путь на 1 секцию с начала и прибавляем элементы из shares
    all_posible_paths = []

    for p_path in sorted(possible_paths, key=len, reverse=True):
        p_path_split = [i for i in p_path.split(os.sep) if i]
        
        for share in shares:
            for i in range(len(p_path_split) + 1):

                all_posible_paths.append(
                    os.path.join(share, *p_path_split[i:])
                    )

    # из всех полученных возможных путей ищем самый подходящий существующий путь
    for i in sorted(all_posible_paths, key=len, reverse=True):
        if os.path.exists(i):
            src_final = i
            break

    # смотрим совпадает ли последняя секция входящего и полученного пути
    tail = []

    if src_final:
        src_final_last = src_final.split(os.sep)[-1]
        if src_splited[-1] != src_final_last:
            tail = src_splited[src_splited.index(src_final_last) + 1:]

    # пытаемся найти секции пути, написанные с ошибкой
    for a in tail:
        dirs = [x for x in os.listdir(src_final)]

        for b in dirs:
            matcher = SequenceMatcher(None, a, b).ratio()
            print(a,b)
            if matcher >= 0.85:
                src_final = os.path.join(src_final, b)
                break

    # print(tail)


src = "\\192.168.10.105\\shares\\Marketing\\General\\9. ТЕКСТЫ\\)2023\\7. PR-рассылка\\10. Октябрь\\Royal"

# b = path_finder(src)

a, b = ")2023" , "2023"
matcher = SequenceMatcher(None, a, b).ratio()
print(matcher)
