from janis_core import File


class Tsv(File):
    def __init__(self, optional=None):
        super().__init__(optional=optional, extension=".tsv")

    @staticmethod
    def name():
        return "tsv"

    def doc(self):
        return "A tab separated file"
