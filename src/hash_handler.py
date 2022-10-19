#!/usr/bin/env python3

from hashlib import sha1
from pathlib import Path


class HashHandler():
    def __init__(self, path: Path) -> None:
        self.__path: Path = path
        if path.exists():
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
        if path.exists():
            self.__hash_hex = self.__calculateHash(self.__path)
        else:
            raise FileNotFoundError

    def __byteReadFile(self, path: Path) -> bytes:
        with open(path.name, 'rb') as file:
            return file.read()

    def __calculateHash(self, path: Path=Path('')) -> str:
        if (path.name == ''):
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
