import os

class Test:
    @classmethod
    def get_sys_volume(cls, volumes: list[str]):
        user = os.path.expanduser("~")
        app_support = os.path.join("Library", "Application Support")
        app_support = os.path.join(user, app_support)

        for i in volumes:
            full_path = os.path.join(i, app_support)
            if os.path.exists(full_path):
                return i

        return None

    @classmethod
    def get_volumes(cls):
        volumes = "/Volumes"
        return [
            i.path
            for i in os.scandir(volumes)
        ]
    
volumes = Test.get_volumes()
sys_ = Test.get_sys_volume(volumes)

print(sys_)