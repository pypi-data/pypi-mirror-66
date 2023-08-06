from janis_core import File


class Csv(File):
    def __init__(self, optional=None):
        super().__init__(optional=optional, extension=".csv")

    @staticmethod
    def name():
        return "csv"

    def doc(self):
        return "A comma separated file"
