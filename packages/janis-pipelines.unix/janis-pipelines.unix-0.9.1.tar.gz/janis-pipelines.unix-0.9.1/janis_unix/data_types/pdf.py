from janis_core import File


class Csv(File):
    def __init__(self, optional=None):
        super().__init__(optional=optional, extension=".pdf")

    @staticmethod
    def name():
        return "pdf"

    def doc(self):
        return "A PDF (Adobe Portable Document Format) file"
