#!/usr/bin/env python3

from os.path import exists
from shutil import copy as shutil_copy
from typing import Dict, Any, List

from json_handler import JsonHandler
from hash_handler import HashHandler

# TODO make adequate import
from filesync_exceptions import CopyDoesNotExistsError, OriginDoesNotExistsError


class FileSync():
    def __init__(self, path: str) -> None:
        self.__json_handler = JsonHandler(path)

    def add(self, origin: str, copy: str) -> None:
       self.__json_handler.add_origin(origin)
       self.__json_handler.add_copy(origin, copy)

    def delete(self, origin: str) -> None:
        self.__json_handler.remove_origin(origin)

    def set_origin_hash(self, origin: str) -> None:
        self.__json_handler.check_existing(origin)
        hasher: HashHandler = HashHandler(origin)
        data: Dict[str, Any] = self.__json_handler.read()
        data[origin]['metadata']['hash'] = hasher.hash()
        self.__json_handler.write(data)

    def set_copy_hash(self, origin: str, copy: str) -> None:
        self.__json_handler.check_existing(origin, copy)
        hasher: HashHandler = HashHandler(copy)
        data: Dict[str, Any] = self.__json_handler.read()
        data[origin]['copies']['hash'] = hasher.hash()
        self.__json_handler.write(data)

    def set_origins_hashes(self) -> None:
        origins: List[str] = self.__json_handler.get_origins()
        origin: str
        for origin in origins:
            self.set_origin_hash(origin)
        self.__json_handler.write(data)
        
    def set_copies_hashes(self) -> None:
        copies: List[str] = self.__json_handler.get_copies()
        copy: str
        for copy in copies:
            self.set_copy_hash(copy)
        self.__json_handler.write(data)

    def update_statuses(self) -> None:
        data: Dict[str, Any] = self.__json_handler.read()
        for origin in data:
            print(origin)
            hasher: HashHandler = HashHandler(origin)
            if data[origin]['metadata']['hash'] != hasher.hash:
                data[origin]['metadata']['changed'] = True
        self.__json_handler.write(data)

    def reset_origins_hash(self) -> None:
        changed_origins: List[str] = self.__json_handler.get_changed_origins()
        origin: str
        for origin in changed_origins:
            slef.set_origin_hash(origin)

    def unset_changed_origins(self) -> None:
        changed_origins: List[str] = self.__json_handler.get_changed_origins()
        data: Dict[str, Any] = self.__json_handler.read()
        origin: str
        for origin in changed_origins:
            data[origin]['metadata']['changed'] = False
        self.__json_handler.write(data)

    def update_copies(self) -> None:
        changed_origins: List[str] = self.__json_handler.get_changed_origins()
        origin: str
        copy: str
        for origin in changed_origins:
            for copy in self.__json_handler.get_copies(origin):
                shutil_copy(origin, copy)

    def sync(self) -> None:
        self.update_statuses()
        self.update_copies()
        self.unset_changed_origins()


    #TODO main methods: comparing, copying

def main() -> None:
    fs = FileSync(r'store.json')
    fs.add(r'test.txt', r'test2.txt')
    fs.sync()

if __name__ == '__main__':
    main()
