from json import dump, load
from os.path import exists
from typing import Dict, Any, List

from filesync_exceptions import CopyDoesNotExistsError, OriginDoesNotExistsError


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

    def exists_origin(self, origin: str) -> bool:
        data: Dict[str, Any] = self.read()
        if data.get(origin):
            return True
        return False

    def exists_copy(self, origin: str, copy: str) -> bool:
        data: Dict[str, Any] = self.read()
        if data[origin]['copies']:
            return True
        return False

    def check_existing(self, origin: str, copy: str=''):
        if not self.exists_origin(origin):
            raise OriginDoesNotExistsError(origin)
        if copy and not self.exists_copy(copy):
            raise CopyDoesNotExistsError(origin, copy)

    def add_origin(self, origin: str) -> None:
        data: Dict[str, Any] = self.read()
        data.update({origin: {'metadata': {'hash': None, 'changed': True},
            'copies': {}}})
        self.write(data)
        
    def add_copy(self, origin: str, copy: str) -> None:
        self.check_existing(origin)
        data: Dict[str, Any] = self.read()
        copy_dict: Dict[str, Dict[str, None]] = {copy: {'hash': None}}
        data[origin]['copies'].update(copy_dict)
        self.write(data);

    def get_origins(self) -> List[str]:
        data: Dict[str, Any] = self.read()
        return list(data.keys())

    def get_copies(self, origin: str) -> List[str]:
        data: Dict[str, Any] = self.read()
        return list(data[origin]['copies'].keys())

    def remove_origin(self, origin: str) -> None:
        self.check_existing(origin)
        data: Dict[str, Any] = self.read()
        data.__delitem__(origin)
        self.write(data)

    def remove_copy(self, origin: str, copy: str) -> None:
        self.check_existing(origin, copy)
        data: Dict[str, Any] = self.read()
        data[origin]['copies'].__delitem__(copy)
        self.write(data)

    def get_changed_origins(self) -> List[str]:
        data: Dict[str, Any] = self.read()
        changed_origins: List[str] = []
        for origin in data:
            if data[origin]['metadata']['changed'] == True:
                changed_origins.append(origin)
        return changed_origins

def main() -> None:
    jh = JsonHandler('store.json')
    jh.add_origin('file1.txt')
    jh.add_origin('file2.txt')
    jh.add_copy('file1.txt', 'file3.txt')
    print(jh.read())


if __name__ == '__main__':
    main()
