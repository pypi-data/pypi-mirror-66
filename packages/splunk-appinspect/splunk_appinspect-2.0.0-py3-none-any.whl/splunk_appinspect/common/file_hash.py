import hashlib


def md5(file_path):
    return hashlib.md5(_file_as_bytes(open(file_path, 'rb'))).hexdigest()


def _file_as_bytes(file):
    with file:
        return file.read()
