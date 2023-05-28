from .stpi import StudentPortalInstance


class Peeps:
    __instance: dict[int, StudentPortalInstance] = {}

    @classmethod
    def fetch(cls, id: int):
        return cls.__instance.get(id)

    @classmethod
    def new(cls, id: int, username: str, password: str):
        assert cls.fetch(id) is None, "User Already logged in!"

        new_peep = StudentPortalInstance(username, password)

        if new_peep.success:
            cls.__instance[id] = new_peep

        return new_peep.success

    @classmethod
    def delete(cls, id: int):
        assert cls.fetch(id) is not None, "User NOT Already logged in!"
        cls.__instance[id].driver.close()
        del cls.__instance[id]
