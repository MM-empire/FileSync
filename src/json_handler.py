from json import dump, load
from os.path import exists
from typing import Dict, Any


class JsonHandler():
    def __init__(self, path: str) -> None:
        self.path: str = path
        if not exists(path):
            self.write({})
            
    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, path: str) -> None:
        if not path.endswith('.json'):
            raise FileNotFoundError
        self.__path = path
    
    def read(self) -> Dict[str, Any]:
        with open(self.path, 'r') as file:
            return load(file)

    def write(self, data: Dict[str, Any]) -> None:
        with open(self.path, 'w') as file:
            dump(data, file, indent=4)

    def add_origin(self, origin_path: str) -> None:
        data: Dict[str, Any] = self.read()
        data.update({origin_path: {'metadata': {'hash': None, 'changed': True},
            'copies': {}}})
        self.write(data)
        
    def add_copy(self, origin_path: str, copy_path: str) -> None:
        data: Dict[str, Any] = self.read()
        copy_dict: Dict[str, Dict[str, None]] = {copy_path: {'hash': None}}
        data[origin_path]['copies'].update(copy_dict)
        self.write(data);


def main() -> None:
    jh = JsonHandler('store.json')
    jh.add_origin('file1.txt')
    jh.add_origin('file2.txt')
    jh.add_copy('file1.txt', 'file3.txt')
    print(jh.read())


if __name__ == '__main__':
    main()
