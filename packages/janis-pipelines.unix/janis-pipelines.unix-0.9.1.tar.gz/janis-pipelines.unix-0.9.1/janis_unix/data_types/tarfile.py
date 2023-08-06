from janis_core import File


class TarFile(File):
    def __init__(self, optional=None):
        super().__init__(optional=optional, extension=".tar")

    @staticmethod
    def name():
        return "TarFile"

    def doc(self):
        return "A tarfile, ending with .tar"


class TarFileGz(File):
    def __init__(self, optional=None):
        super().__init__(optional=optional, extension=".tar.gz")

    @staticmethod
    def name():
        return "CompressedTarFile"

    def doc(self):
        return "A gzipped tarfile"
