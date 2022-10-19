#!/usr/bin/env python3
from json import dump, load
#  from os.path import exists
from pathlib import Path
from typing import Dict, Any


class JsonHandler():
    def __init__(self, path: Path) -> None:
        self.__path: Path = path
        if not path.exists():
            self.write({})
            
    @property
    def path(self) -> Path:
        return self.__path

    @path.setter
    def path(self, path: Path) -> None:
        self.__path = path
    
    def read(self) -> Dict[Path, Any]:
        with open(self.path, 'r') as file:
            data: Dict[Path, Any] = load(file)
        return data

    def write(self, data: Dict[Path, Any]) -> None:
        with open(self.path, 'w') as file:
            dump(data, file, indent=4)

    def add_origin(self, origin_path: Path) -> None:
        data: Dict[Path, Any] = self.read()
        data.update({origin_path: {'metadata': {'hash': None, 'changed': True},
            'copies': {}}})
        self.write(data)
        
    def add_copy(self, origin_path: Path, copy_path: Path) -> None:
        data: Dict[Path, Any] = self.read()
        copy_dict: Dict[Path, Dict[str, None]] = {copy_path: {'hash': None}}
        data[origin_path]['copies'].update(copy_dict)
        self.write(data);


def main() -> None:
    jh = JsonHandler(Path('store.json'))
    jh.add_origin(Path('file1.txt'))
    jh.add_origin(Path('file2.txt'))
    jh.add_copy(Path('file1.txt'), Path('file3.txt'))
    print(jh.read())


if __name__ == '__main__':
    main()
