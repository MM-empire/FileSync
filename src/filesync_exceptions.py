class CopyDoesNotExistsError(Exception):
    def __init__(self, origin: str, copy: str):
        message: str = f'"{copy}" is not in copies of "{origin}".'
        super().__init__(message)

class OriginDoesNotExistsError(Exception):
    def __init__(self, origin: str):
        message: str = f'"{origin}" is not in origins.'
        super().__init__(message)


def main() -> None:
    raise OriginDoesNotExistsError('origin')
    raise CopyDoesNotExistsError('origin', 'copy')

if __name__ == '__main__':
    main()
