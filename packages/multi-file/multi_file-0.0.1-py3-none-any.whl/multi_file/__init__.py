import tarfile
from tempfile import NamedTemporaryFile


class MultiFile:
    def __init__(self, fh, mode):
        self.tar = tarfile.TarFile(fileobj=fh, mode=mode)
        self.mode = mode

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.tar.close()

    def open(self, key, binary=True):
        if self.mode == 'w':
            return MultiFileWriter(self, key, binary)
        elif self.mode == 'r':
            member = self.tar.getmember(key)
            return self.tar.extractfile(member)

    def __contains__(self, key):
        try:
            self.tar.getmember(key)
            return True
        except KeyError:
            return False

    def keys(self):
        return self.tar.getnames()


class MultiFileWriter:
    def __init__(self, multifile, key, binary):
        self.multifile = multifile
        self.key = key
        self.binary = binary

    def __enter__(self):
        mode = 'w+b' if self.binary else 'w'
        self.tempfile = NamedTemporaryFile(mode, delete=False)
        return self.tempfile

    def __exit__(self, type, value, traceback):
        self.tempfile.seek(0)
        self.multifile.tar.add(self.tempfile.name, self.key)
        self.tempfile.close()
