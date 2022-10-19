from pathlib import Path


class CopyDoesNotExistsError(Exception):
    def __init__(self, origin: Path, copy: Path):
        message: str = f'"{copy.name}" is not in copies of "{origin.name}".'
        super().__init__(message)

class OriginDoesNotExistsError(Exception):
    def __init__(self, origin: Path):
        message: str = f'"{origin.name}" is not in origins.'
        super().__init__(message)


def main() -> None:
    origin = Path('origin')
    copy = Path('copy')
    raise CopyDoesNotExistsError(origin, copy)

if __name__ == '__main__':
    main()
