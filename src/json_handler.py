#!/usr/bin/env python3
from json import dump, load
from pathlib import Path
from typing import Dict, Any, List, Optional

from exceptions import CopyDoesNotExistsError, \
        OriginDoesNotExistsError


class JsonHandler():
    def __init__(self, path: Path) -> None:
        self.path: Path = path
        if not path.exists():
            self.write({})

    @property
    def path(self) -> Path:
        return self.__path

    @path.setter
    def path(self, path: Path) -> None:
        if not str(path).endswith('.json'):
            raise FileNotFoundError
        self.__path = path
    
    def read(self) -> Dict[str, Any]:
        with open(str(self.path), 'r') as file:
            return load(file)

    def write(self, data: Dict[str, Any]) -> None:
        with open(str(self.path), 'w') as file:
            dump(data, file, indent=4)

    def exists_origin(self, origin: Path) -> bool:
        data: Dict[str, Any] = self.read()
        if data.get(str(origin)):
            return True
        return False

    def exists_copy(self, origin: Path, copy: Path) -> bool:
        """
        Return True if origin and its copy are exists
        """
        data: Dict[str, Any] = self.read()
        if data[str(origin)]['copies'] and copy in self.get_copies(origin):
            return True
        return False

    def check_existing(self, origin: Path, copy: Optional[Path]=None):
        if not self.exists_origin(origin):
            raise OriginDoesNotExistsError(origin)
        if copy and not self.exists_copy(origin, copy):
            # print(str(copy))
            raise CopyDoesNotExistsError(origin, copy)

    def add_origin(self, origin: Path) -> None:
        if not self.exists_origin(origin):
            origin_dict: Dict[str, Any] = {str(origin): {'metadata': \
                    {'hash': None, 'changed': True}, 'copies': {}}}
            data: Dict[str, Any] = self.read()
            data.update(origin_dict)
            self.write(data)
        
    def add_copy(self, origin: Path, copy: Path) -> None:
        self.check_existing(origin)
        if not self.exists_copy(origin, copy):
            data: Dict[str, Any] = self.read()
            copy_dict: Dict[str, Dict[str, None]] = {str(copy): {'hash': None}}
            data[str(origin)]['copies'].update(copy_dict)
            self.write(data);

    def get_origins(self) -> List[Path]:
        data: Dict[str, Any] = self.read()
        return [Path(path) for path in data.keys()]

    def get_copies(self, origin: Path) -> List[Path]:
        data: Dict[str, Any] = self.read()
        return [Path(path) for path in data[str(origin)]['copies'].keys()]

    def remove_origin(self, origin: Path) -> None:
        self.check_existing(origin)
        data: Dict[str, Any] = self.read()
        data.__delitem__(str(origin))
        self.write(data)

    def remove_copy(self, origin: Path, copy: Path) -> None:
        self.check_existing(origin, copy)
        data: Dict[str, Any] = self.read()
        data[str(origin)]['copies'].__delitem__(str(copy))
        self.write(data)

    def get_changed_origins(self) -> List[Path]:
        data: Dict[str, Any] = self.read()
        changed_origins: List[Path] = [Path(path) for path in
                data if data[path]['metadata']['changed'] == True]

        return changed_origins

    def get_all_changed_copies(self):
        """
        Return list with origin paths and all copies paths
        With a structure [origin, [copy]]
        """
        data: Dict[str, Any] = self.read()
        changed_copies: List[Path] = []
        for origin in data:
            copies_list: List[Path] = []
            flag_changed = False
            for copy in data[origin]['copies']:
                if data[origin]['metadata']['hash'] != data[origin]['copies'][copy]['hash']:
                    copies_list.append(Path(copy))
                    flag_changed = True
            if flag_changed:
                changed_copies.append([Path(origin), copies_list])
        
        return changed_copies

    def get_changed_copies(self, origin: Path):
        """
        Return list of all copies paths of this origin
        With a structure [copy]
        """
        data: Dict[str, Any] = self.read()
        origin = self.get_copies(origin)
        copies_list: List[Path] = []
        for copy in data[origin]['copies']:
            if data[origin]['metadata']['hash'] != data[origin]['copies'][copy]['hash']:
                copies_list.append(Path(copy))
        
        return copies_list


def main() -> None:
    jh = JsonHandler(Path('store.json'))
    jh.add_origin(Path('file.file'))
    # jh.add_origin(Path('/home/user/sandbox/python/file.txt'))
    # jh.add_copy(Path('file1.txt'), Path('file3.txt'))
    jh.add_copy()
    print(jh.exists_copy(Path('file.file'), Path('test-dir/file.file')))
    # print(jh.read())


if __name__ == '__main__':
    main()
