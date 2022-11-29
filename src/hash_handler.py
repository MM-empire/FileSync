#!/usr/bin/env python3

from hashlib import sha1
from os.path import exists


class HashHandler():
    def __init__(self, path: str) -> None:
        self.__path: str = path
        if exists(path):
            self.__hash_hex: str = self.__calculateHash(self.__path)
        else:
            pass

    @property
    def hash(self) -> str:
        return self.__hash_hex

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, path: str) -> None:
        self.__path = path
        if exists(path):
            self.__hash_hex = self.__calculateHash(self.__path)
        else:
            pass

    def compareHash(self, comp_file_path: str) -> bool:
        if (self.__hash_hex == self.__calculateHash(comp_file_path)):
            return True

        return False

    def __byteReadFile(self, path: str) -> bytes:
        with open(path, 'rb') as file:
            return file.read()

    @staticmethod
    def calculate_hash(path: Path, algorithm: str = 'sha1') -> str:
        buf: bytes = HashHandler.__byte_read_file(path)
        hasher = new(algorithm)
        hasher.update(buf)
        hash_hex = hasher.hexdigest()
        return hash_hex


def main() -> None:
    # file1.file does not exists
    h = HashHandler("file1.file")
    h = HashHandler("file2.file")
    h.path = "file.file"
    print(h.compareHash("file2.file"))
    print(h.hash)
    print(h.path)

    """
    TODO:
    1. Check if compare file is exists
    """


if __name__ == "__main__":
    main()
