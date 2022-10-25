#!/usr/bin/env python3

from pathlib import Path


class CopyDoesNotExistsError(Exception):
    def __init__(self, origin: Path, copy: Path):
        message: str = f'"{str(copy)}" is not in copies of "{str(origin)}".'
        super().__init__(message)

class OriginDoesNotExistsError(Exception):
    def __init__(self, origin: Path):
        message: str = f'"{str(origin)}" is not in origins.'
        super().__init__(message)


def main() -> None:
    origin = Path('origin/samples/origin.py')
    copy = Path('copies/copy.py')
    raise CopyDoesNotExistsError(origin, copy)

if __name__ == '__main__':
    main()
