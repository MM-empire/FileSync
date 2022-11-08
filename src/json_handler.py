#!/usr/bin/env python3
from json import dump, load
from pathlib import Path
from typing import Dict, Any, List, Optional

from exceptions import CopyDoesNotExistsError, \
        OriginDoesNotExistsError, FileIsNotJsonError


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
            raise FileIsNotJsonError
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

    def check_existing(self, origin: Path, copy: Optional[Path] = None):
        if not self.exists_origin(origin):
            raise OriginDoesNotExistsError(origin)
        if copy and not self.exists_copy(origin, copy):
            # print(str(copy))
            raise CopyDoesNotExistsError(origin, copy)

    def add_origin(self, origin: Path) -> None:
        if not self.exists_origin(origin):
            origin_dict: Dict[str, Any] = {
                str(origin): {
                    'hash': None,
                    'copies': {}}
            }
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

    def get_all_changed_origins(self) -> List[Path]:
        data: Dict[str, Any] = self.read()
        all_changed_origins: List[Path] = []
        origin: Path
        for origin in self.get_origins():
            copies = self.get_copies(origin)
            is_changed: bool = False
            for copy in copies:
                if data[str(origin)]['hash'] != \
                        data[str(origin)]['copies'][str(copy)]['hash']:
                    is_changed = True

            if is_changed:
                all_changed_origins.append(origin)

        return all_changed_origins

    def get_all_changed_copies(self) -> List[Path]:
        """
        Return list with origin paths and all copies paths
        With a structure [origin, [copy]]
        """
        origins: List[Path] = self.get_origins()
        all_changed_copies: List[Path] = []
        origin: Path
        for origin in origins:
            all_changed_copies.extend(self.get_changed_copies(origin))

        return all_changed_copies

    def get_changed_copies(self, origin: Path) -> List[Path]:
        """
        Return list of all copies paths of this origin
        With a structure [copy]
        """
        data: Dict[str, Any] = self.read()
        copies: List[Path] = self.get_copies(origin)
        copies_list: List[Path] = []
        for copy in copies:
            if data[str(origin)]['hash'] != \
                    data[str(origin)]['copies'][str(copy)]['hash']:
                copies_list.append(copy)

        return copies_list

    def compare_hashes(self, origin: Path, copy: Path) -> bool:
        """
        Return True if hashes are the same
        Return False if hashes are different
        """
        self.check_existing(origin, copy)
        data: Dict[str, Any] = self.read()
        origin_str: str = str(origin)
        copy_str: str = str(copy)
        return data[origin_str]['hash'] == \
            data[origin_str]['copies'][copy_str]['hash']


def main() -> None:
    jh = JsonHandler(Path('synclist.json'))
    # jh.add_origin(Path('file.file'))
    # jh.add_origin(Path('/home/user/sandbox/python/file.txt'))
    # jh.add_copy(Path('file.file'), Path('file3.txt'))
    # print(jh.exists_copy(Path('file.file'), Path('file3.txt')))
    # jh.add_origin(Path('/home/user/sandbox/python/file.txt'))
    # jh.add_copy(Path('file.file'), Path('file3.txt'))
    # jh.get_changed_copies('file.file')
    # jh.get_all_changed_copies()
    # print(jh.exists_copy(Path('file.file'), Path('test-dir/file.file')))
    # print(jh.get_copies("/home/mikhail/repos/FileSync/src/file.file"))
    print(jh.get_all_changed_origins)


if __name__ == '__main__':
    main()
