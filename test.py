import os


def get_shares():
    return [
        os.path.join("/Volumes", i)
        for i in os.listdir("/Volumes")
        if os.path.ismount(os.path.join("/Volumes", i))
        ]


def normalize_path(path: str):
    return os.sep + path.replace("\\", os.sep).strip().strip(os.sep)


def generate_paths(shares: list, splited_path: list):
    paths = []
    limit = len(splited_path) + 1

    for share in shares:
        for i in range(0, limit):
            paths.append(share + splited_path[i:])
            paths.append(os.path.join(share, *splited_path[:i]))

    return paths


def check_path(path_list: list):
    for i in sorted(path_list, key=len, reverse=True):
        if os.path.exists(i):
            return i
    return False

def compare_end_paths(a: str, b: str):
    if a.split(os.sep)[-1] == b.split(os.sep)[-1]:
        return True
    return False


src = "/Volumes/Shares-1/Marketing/Design/STORES_МАГАЗИНЫ/LSM/2024/Master/Artwork/Печать1"
src = normalize_path(src)
shares = get_shares()
# path_list = generate_paths(shares, src.split(os.sep))
# checked = check_path(path_list)

print(shares)