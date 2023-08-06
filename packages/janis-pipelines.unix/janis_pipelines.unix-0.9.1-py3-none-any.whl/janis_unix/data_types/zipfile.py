from janis_core import File


class ZipFile(File):
    def __init__(self, optional=None):
        super().__init__(optional=optional, extension=".zip")

    @staticmethod
    def name():
        return "Zip"

    def doc(self):
        return "A zip archive, ending with .zip"
