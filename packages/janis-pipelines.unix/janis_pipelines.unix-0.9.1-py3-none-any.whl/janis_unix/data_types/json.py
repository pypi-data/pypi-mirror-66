from janis_core import File


class JsonFile(File):
    def __init__(self, optional=None):
        super().__init__(optional=optional, extension=".json")

    @staticmethod
    def name():
        return "jsonFile"

    def doc(self):
        return "A JSON file file"
