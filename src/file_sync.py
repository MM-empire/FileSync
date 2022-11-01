#!/usr/bin/env python3

from pathlib import Path
from shutil import copy as shutil_copy
from typing import Dict, Any, List, Union, Optional

from json_handler import JsonHandler
from hash_handler import HashHandler

from exceptions import CopyDoesNotExistsError, \
        OriginDoesNotExistsError


#TODO main methods: comparing, copying
#TODO resolve path start with no ./
class FileSync():
    """
    File Sync class that allaw to:
        - add
        - delete
        - sync
    """
    def __init__(self, path: Path=Path('store.json')) -> None:
        self.__json_handler = JsonHandler(path)

    # set mapping for *copies
    def add(self, origin: Path, copies: List[Path]) -> None:
        """
        Add origin and its copies to sync list
        """
        origin = origin.resolve()
        self.__json_handler.add_origin(origin)
        self.__set_origin_hash(origin)
        copy: Path
        for copy in copies:
            copy = copy.resolve()
            self.__json_handler.add_copy(origin, copy)
            if copy.is_file():
               self.__set_copy_hash(origin, copy)

    # set mapping for *copies
    def delete(self, origin: Path, *copies: Union[Path, List[Path]]) -> None:
        """
        Delete origin and its copies
        If no copies delete origin from sync list
        else delete copies of origin
        """
        if not copies:
            self.__json_handler.remove_origin(origin)
        else:
            copy: Path
            for copy in copies:
                # TODO: add exceptions
                self.__json_handler.remove_copy(origin, copy)

    def set_copies_hashes(self, origin: Path) -> None:
        """
        Update hashs for origin copies
        """
        copies: List[Path] = self.__json_handler.get_copies(origin)
        copy: Path
        for copy in copies:
            self.__set_copy_hash(origin, copy)

    def update_hashes(self) -> None:
        """
        Update hashs for all origins and their copies
        """
        data: Dict[str, Any] = self.__json_handler.read()
        for origin in data:
            for copy in data[origin]['copies']:
                self.__create_file(copy)
            self.set_copies_hashes(origin)

    def sync_all(self) -> None:
        """
        Synchronize all copies of all origins
        """
        self.__update_statuses()
        self.update_hashes()
        self.__update_copies()
        self.__unset_changed_origins()

        changed: [Path, List[Path]]
        for changed in self.__json_handler.get_all_changed_copies():
            for copy in changed[1]:
                shutil_copy(str(changed[0]), str(copy))

        self.update_hashes()

    def sync(self, origin: Path) -> None:
        """
        Synchronize copies of origin
        """
        origin = origin.resolve()
        self.__update_statuses()
        self.update_hashes()
        self.__update_copies()
        self.__unset_changed_origins()

        for p in self.__json_handler.get_copies(origin):
            shutil_copy(origin, str(p))
            
        self.update_hashes()

    def get_origins(self) -> List[Path]:
        """
        Return list of all origins paths
        """
        return [Path(origin).resolve() for origin in self.__json_handler.get_origins()]
        # return self.__json_handler.get_origins()

    def get_copies(self, origin: Path) -> List[Path]:
        """
        Return copies paths of origin
        """
        origin = origin.resolve()
        return self.__json_handler.get_copies(origin)

    def compare_hashes(self, origin: Path, copy: Path) -> bool:
        """
        Return True if hashes are the same
        Return False if hashes are different
        """
        # TODO: wrap exception
        return self.__json_handler.compare_hashes(origin, copy)

    def __set_origin_hash(self, origin: Path) -> None:
        """
        Set hash for origin
        """
        self.__json_handler.check_existing(origin)
        _hash: str = HashHandler.calculate_hash(origin)
        data: Dict[str, Any] = self.__json_handler.read()
        data[str(origin)]['metadata']['hash'] = _hash
        self.__json_handler.write(data)

    def __set_copy_hash(self, origin: Path, copy: Optional[Path]) -> None:
        """
        Set hash for copy of origin
        """
        self.__json_handler.check_existing(origin, copy)
        _hash: str = HashHandler.calculate_hash(copy)
        data: Dict[str, Any] = self.__json_handler.read()
        data[str(origin)]['copies'][str(copy)]['hash'] = _hash
        self.__json_handler.write(data)

    def __set_origins_hashes(self) -> None:
        """
        Set hashes for all origins
        """
        origins: List[Path] = self.__json_handler.get_origins()
        origin: Path
        for origin in origins:
            self.__set_origin_hash(origin)
        
    def __update_statuses(self) -> None:
        """
        Set 'changed' flag True for all origins if they are different for current origins
        """
        data: Dict[str, Any] = self.__json_handler.read()
        for origin in data:
            _hash_origin: str = HashHandler.calculate_hash(Path(origin))
            if data[origin]['metadata']['hash'] != _hash_origin:
                data[origin]['metadata']['changed'] = True

        self.__json_handler.write(data)

    def __unset_changed_origins(self) -> None:
        changed_origins: List[Path] = self.__json_handler.get_changed_origins()
        data: Dict[str, Any] = self.__json_handler.read()
        origin: Path
        for origin in changed_origins:
            data[str(origin)]['metadata']['changed'] = False
        self.__json_handler.write(data)

    def __update_copies(self) -> None:
        """
        Copy changed origins to all its copy
        """
        changed_origins: List[Path] = self.__json_handler.get_changed_origins()
        origin: Path
        copy: Path
        for origin in changed_origins:
            for copy in self.__json_handler.get_copies(origin):
                shutil_copy(str(origin), str(copy))

    def __create_file(self, path: str):
        """
        Create file if it does not exsists
        """
        if not Path(path).is_file():
            with open(path, 'x') as f:
                pass


def main() -> None:
    jsn: Path = Path('store.json')
    origin: Path = Path('file2.file').resolve()
    copy: Path = [Path('./test-dir/file2.new'), 
                  Path('./test-dir/file2.file')]
    fs = FileSync(jsn)
    for o in fs.get_origins():
        print(fs.get_copies(o))
    # print(fs.list_all())
    # print(type(origin))
    # print(origin)
    # print(fs.get_copies(origin))
    # print(str(origin))
    # fs.update_hashes()
    # fs.add(origin, copy)
    # fs.sync_two_files(origin, copy)
    # fs.full_sync()
    # fs.sync()

if __name__ == '__main__':
    main()
