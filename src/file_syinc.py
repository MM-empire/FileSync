#!/usr/bin/env python3

from pathlib import Path
from shutil import copy as shutil_copy
from typing import Dict, Any, List

from json_handler import JsonHandler
from hash_handler import HashHandler

from filesync_exceptions import CopyDoesNotExistsError, \
        OriginDoesNotExistsError

class FileSync():
    def __init__(self, path: Path) -> None:
        self.__json_handler = JsonHandler(path)

    def add(self, origin: str, copy: str) -> None:
       self.__json_handler.add_origin(origin)
       self.__json_handler.add_copy(origin, copy)

    def delete(self, origin: Path) -> None:
        self.__json_handler.remove_origin(origin)

    def set_origin_hash(self, origin: Path) -> None:
        self.__json_handler.check_existing(origin.name)
        hasher: HashHandler = HashHandler(origin.name)
        data: Dict[Path, Any] = self.__json_handler.read()
        data[origin.name]['metadata']['hash'] = hasher.hash()
        self.__json_handler.write(data)

    def set_copy_hash(self, origin: Path, copy: Path) -> None:
        self.__json_handler.check_existing(origin.name, copy)
        hasher: HashHandler = HashHandler(copy)
        data: Dict[Path, Any] = self.__json_handler.read()
        data[origin.name]['copies']['hash'] = hasher.hash()
        self.__json_handler.write(data)

    def set_origins_hashes(self) -> None:
        origins: List[Path] = self.__json_handler.get_origins()
        origin: Path
        for origin in origins:
            self.set_origin_hash(origin.name)
        self.__json_handler.write(data)
        
    def set_copies_hashes(self) -> None:
        copies: List[Path] = self.__json_handler.get_copies()
        copy: Path
        for copy in copies:
            self.set_copy_hash(copy.name)
        self.__json_handler.write(data)

    def update_statuses(self) -> None:
        data: Dict[str, Any] = self.__json_handler.read()
        for origin in data:
            hasher: HashHandler = HashHandler(origin)
            if data[origin]['metadata']['hash'] != hasher.hash:
                data[origin]['metadata']['changed'] = True
        self.__json_handler.write(data)

    def unset_changed_origins(self) -> None:
        changed_origins: List[Path] = self.__json_handler.get_changed_origins()
        data: Dict[str, Any] = self.__json_handler.read()
        origin: Path
        for origin in changed_origins:
            data[origin.name]['metadata']['changed'] = False
        self.__json_handler.write(data)

    def update_copies(self) -> None:
        changed_origins: List[Path] = self.__json_handler.get_changed_origins()
        origin: Path
        copy: Path
        for origin in changed_origins:
            for copy in self.__json_handler.get_copies(origin):
                shutil_copy(origin.name, copy.name)

    def sync(self) -> None:
        self.update_statuses()
        self.update_copies()
        self.unset_changed_origins()


    #TODO main methods: comparing, copying

def main() -> None:
    jsn: Path = Path('store.json')
    origin: Path = Path('/home/user/sandbox/python/test.txt')
    copy: Path = Path('test.txt')
    fs = FileSync(jsn)
    fs.add(origin, copy)
    fs.sync()

if __name__ == '__main__':
    main()
