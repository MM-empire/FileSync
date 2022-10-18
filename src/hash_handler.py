#!/usr/bin/env python3

from hashlib import sha1
from os.path import exists


class HashHandler():
    def __init__(self, path: str) -> None:
        self.__path: str = path
        if exists(path):
            self.__hash_hex: str = self.__calculateHash(self.__path)
        else:
            raise FileNotFoundError

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
        flag: bool = False
        if (self.__hash_hex == self.__calculateHash(comp_file_path)):
            flga = True

        return flag

    def __byteReadFile(self, path: str) -> bytes:
        with open(path, 'rb') as file:
            return file.read()

    def __calculateHash(self, path: str = '') -> str:
        if (path == ''):
            path = self.__path

        buf: bytes = self.__byteReadFile(path)
        hasher = sha1()
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
