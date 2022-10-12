from json import dump, load
from os.path import exists
from typing import Dict, Any


class JsonHandler():
    def __init__(self, path: str) -> None:
        self.__path: str = path
        if not exists(path):
            self.write({})
            
    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, path: str) -> None:
        self.__path = path
    
    def read(self) -> Dict[str, Any]:
        with open(self.path, 'r') as file:
            data: Dict[str, Any] = load(file)
        return data

    def write(self, data: Dict[str, Any]) -> None:
        with open(self.path, 'w') as file:
            dump(data, file, indent=4)

    def add_origin(self, path: str) -> None:
        data: Dict[str, Any] = self.read()
        data.update({path: {'metadata': {'hash': None, 'changed': True},
            'clones': {}}})
        self.write(data)
        
    def add_clone(self, origin: str, clone: str) -> None:
        data: Dict[str, Any] = self.read()
        clone_dict: Dict[str, Dict[str, None]] = {clone: {'hash': None}}
        data[origin]['clones'].update(clone_dict)
        self.write(data);


def main() -> None:
    jh = JsonHandler('store.json')
    jh.add_origin('file1.txt')
    jh.add_origin('file2.txt')
    jh.add_clone('file1.txt', 'file3.txt')
    print(jh.read())


if __name__ == '__main__':
    main()
