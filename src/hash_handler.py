#!/usr/bin/env python3

from hashlib import new
from pathlib import Path


class HashHandler():
    @staticmethod
    def __byte_read_file(path: Path) -> bytes:
        with open(str(path), 'rb') as file:

            return file.read()

    @staticmethod
    def calculate_hash(path: Path, algorithm: str='sha1') -> str:
        buf: bytes = HashHandler.__byte_readFile(path)
        hasher = new(algorithm)
        hasher.update(buf)
        hash_hex = hasher.hexdigest()
        return hash_hex


def main() -> None:
    # file1.file does not exists
    print(HashHandler.calculate_hash(Path("file.txt")))

    """
    TODO:
    1. Check if compare file is exists
    """

if __name__ == "__main__":
    main()
