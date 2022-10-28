#!/usr/bin/env python3

from pathlib import Path
from shutil import copy as shutil_copy
from typing import Dict, Any, List, Union, Optional

from json_handler import JsonHandler
from hash_handler import HashHandler

from exceptions import CopyDoesNotExistsError, \
        OriginDoesNotExistsError


class FileSync():
    def __init__(self, path: Path=Path('store.json')) -> None:
        self.__json_handler = JsonHandler(path)

    # set mapping for *copies
    def add(self, origin: Path, copies: List[Path]) -> None:
       self.__json_handler.add_origin(origin)
       self.__set_origin_hash(origin)
       copy: Path
       for copy in copies:
           self.__json_handler.add_copy(origin, copy)
           if copy.is_file():
               self.__set_copy_hash(origin, copy)

    # set mapping for *copies
    def delete(self, origin: Path, *copies: Union[Path, List[Path]]) -> None:
        if not copies:
            self.__json_handler.remove_origin(origin)
        else:
            copy: Path
            for copy in copies:
                self.__json_handler.remove_copy(origin, copy)

    def __set_origin_hash(self, origin: Path) -> None:
        self.__json_handler.check_existing(origin)
        _hash: str = HashHandler.calculate_hash(origin)
        data: Dict[str, Any] = self.__json_handler.read()
        data[str(origin)]['metadata']['hash'] = _hash
        self.__json_handler.write(data)

    def __set_copy_hash(self, origin: Path, copy: Optional[Path]) -> None:
        self.__json_handler.check_existing(origin, copy)
        _hash: str = HashHandler.calculate_hash(copy)
        data: Dict[str, Any] = self.__json_handler.read()
        data[str(origin)]['copies'][str(copy)]['hash'] = _hash
        self.__json_handler.write(data)

    def set_origins_hashes(self) -> None:
        origins: List[Path] = self.__json_handler.get_origins()
        origin: Path
        for origin in origins:
            self.__set_origin_hash(origin)
        
    def set_copies_hashes(self, origin: Path) -> None:
        copies: List[Path] = self.__json_handler.get_copies(origin)
        copy: Path
        for copy in copies:
            self.__set_copy_hash(origin, copy)

    def update_hashes(self) -> None:
        data: Dict[str, Any] = self.__json_handler.read()
        for origin in data:
            for copy in data[origin]['copies']:
                self.__create_file(copy)
            self.set_copies_hashes(origin)

    def update_statuses(self) -> None:
        data: Dict[str, Any] = self.__json_handler.read()
        for origin in data:
            _hash_origin: str = HashHandler.calculate_hash(Path(origin))
            if data[origin]['metadata']['hash'] != _hash_origin:
                data[origin]['metadata']['changed'] = True

        self.__json_handler.write(data)

    def unset_changed_origins(self) -> None:
        changed_origins: List[Path] = self.__json_handler.get_changed_origins()
        data: Dict[str, Any] = self.__json_handler.read()
        origin: Path
        for origin in changed_origins:
            data[str(origin)]['metadata']['changed'] = False
        self.__json_handler.write(data)

    def update_copies(self) -> None:
        changed_origins: List[Path] = self.__json_handler.get_changed_origins()
        origin: Path
        copy: Path
        for origin in changed_origins:
            for copy in self.__json_handler.get_copies(origin):
                shutil_copy(str(origin), str(copy))

    def sync_two_files(self, origin: Path, copy: Path):
        self.__json_handler.check_existing(origin, copy)
        shutil_copy(str(origin), str(copy))
        self.__set_copy_hash(origin, copy)

    def full_sync(self) -> None:
        self.update_statuses()
        self.update_copies()
        self.unset_changed_origins()

    def sync(self) -> None:
        self.update_statuses()
        self.update_hashes()
        self.update_copies()
        self.unset_changed_origins()

        changed: [Path, List[Path]]
        for changed in self.__json_handler.get_changed_copies():
            for copy in changed[1]:
                print(changed[0], copy)
                shutil_copy(str(changed[0]), str(copy))

        self.update_hashes()

    def __create_file(self, path: str):
        if not Path(path).is_file():
            with open(path, 'x') as f:
                pass


    #TODO main methods: comparing, copying
    #TODO resolve path start with no ./

def main() -> None:
    jsn: Path = Path('store.json')
    origin: Path = Path('file2.file')
    copy: Path = [Path('./test-dir/file2.new'), 
                  Path('./test-dir/file2.file')]
    # fs = FileSync(jsn)
    # fs.update_hashes()
    # fs.add(origin, copy)
    # fs.sync_two_files(origin, copy)
    # fs.full_sync()
    # fs.sync()

if __name__ == '__main__':
    main()
