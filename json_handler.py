from json import dump, load
from typing import Dict, Union


class JsonHandler():
    def __init__(self, path: str) -> None:
        self.__path: str = path

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, path: str) -> None:
        self.__path = path
    
    def read(self) -> Dict[str, Union[str, bool, None]]:
        with open(self.path, 'r') as file:
            data: Dict[str, Union[str, bool, None]] = load(file)
        return data

    def write(self, data: Dict[str, Union[str, bool, None]]) -> None:
        with open(self.path, 'w') as file:
            dump(data, file)
