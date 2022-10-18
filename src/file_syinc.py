#!/usr/bin/env python3

from os.path import exists
from shutil import copytree
from typing import Dict, Any

from json_handler import JsonHandler
from hash_handler import HashHandler
from filesync_exceptions import CopyDoesNotExistsError, \ OriginDoesNotExistsError


class FileSync():
    def __init__(self, path: str) -> None:
        self.__json_handler = JsonHandler(path)

    def set_origin_hash(self, origin: str) -> None:
        self.__json_handler.check_existing(origin)
        hasher: HashHandler = HashHandler(origin)
        data: Dict[str, Any] = self.__json_handler.read()
        data[origin]['metadata']['hash'] = hasher.hash()
        self.__json_handler.write()

    def set_copy_hash(self, origin: str, copy: str) -> None:
        self.__json_handler.check_existing(origin, copy)
        hasher: HashHandler = HashHandler(copy)
        data: Dict[str, Any] = self.__json_handler.read()
        data[origin]['copies']['hash'] = hasher.hash()
        self.__json_handler.write()
        
    def add(self, origin: str, copy: str) -> None:
       self.__json_handler.add_origin(origin)
       self.__json_handler.add_copy(source, copy)

