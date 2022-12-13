#!/usr/bin/env python3

from pathlib import Path
from os import environ
from shutil import copy as shutil_copy
from typing import Dict, Any, List, Union, Optional

from json_handler import JsonHandler
from hash_handler import HashHandler

from exceptions import CopyDoesNotExistsError, \
        OriginDoesNotExistsError, FileIsNotJsonError


#TODO resolve path start with no ./
class FileSync():
    """
    File Sync class that allaw to:
        - add
        - delete
        - sync
    """
    def __init__(self, path: Optional[Path] = None) -> None:
        self.set_synclist(path)

    # set mapping for *copies
    def add(self, origin: Path, copies: List[Path]) -> None:
        """
        Add origin and its copies to sync list
        """
        origin = origin.resolve()
        self.add_origin(origin)
        copy: Path
        for copy in copies:
            copy = copy.resolve()
            self.__json_handler.add_copy(origin, copy)
            if copy.is_file():
                self.__set_copy_hash(origin, copy)

    def add_origin(self, origin: Path) -> None:
        """
        Add origin and its copies to sync list
        """
        origin = origin.resolve()
        self.__json_handler.add_origin(origin)
        self.__set_origin_hash(origin)

    # set mapping for *copies
    def delete(self, origin: Path, *copies: List[Path]) -> None:
        """
        Delete origin and its copies
        If no copies delete origin from sync list
        else delete copies of origin
        Only remove note from synclist
        """
        if not copies:
            try:
                self.__json_handler.remove_origin(origin)
            except OriginDoesNotExistsError:
                print(f'{str(origin)} is not in synclist')
        else:
            copy: Path
            for copy in copies[0]:
                try:
                    self.__json_handler.remove_copy(origin, copy)
                except OriginDoesNotExistsError:
                    print(f'{str(origin)} is not in synclist')
                except CopyDoesNotExistsError:
                    print(f'{str(copy)} is not a copy of {str(origin)}')

    def set_copies_hashes(self, origin: Path) -> None:
        """
        Update hashs for origin copies
        """
        copies: List[Path] = self.__json_handler.get_copies(origin)
        copy: Path
        for copy in copies:
            self.__set_copy_hash(origin, copy)

    def update_all_hashes(self) -> None:
        """
        Update hashs for all origins and their copies
        """
        for origin in self.get_origins():
            for copy in self.get_copies(origin):
                self.__create_file(copy)
            self.set_copies_hashes(origin)

    def sync_all(self) -> None:
        """
        Synchronize all copies of all origins
        """
        self.update_all_hashes()
        self.__update_copies()

        for origin in self.__json_handler.get_origins():
            for copy in self.__json_handler.get_changed_copies(origin):
                shutil_copy(str(origin), str(copy))

        self.update_all_hashes()

    def sync(self, origin: Path) -> None:
        """
        Synchronize copies of origin
        """
        origin = origin.resolve()
        self.update_all_hashes()
        self.__update_copies()

        for p in self.__json_handler.get_copies(origin):
            shutil_copy(origin, str(p))

        self.update_all_hashes()

    def get_origins(self) -> List[Path]:
        """
        Return list of all origins paths
        """
        return [Path(origin).resolve() for origin in self.__json_handler.get_origins()]

    def get_copies(self, origin: Path) -> List[Path]:
        """
        Return copies paths of origin
        """
        origin = origin.resolve()
        return self.__json_handler.get_copies(origin)

    # TODO: make usable flags
    def get_copy_status(self, origin: Path, copy: Path) -> str:
        """
        Return status of copy for given origin
        Statuses:
            1) same - same hashes of origin and copy
            2) different - different hashes of origin and copy
            3) no copy - copy does not exsists as file
        """
        if (not copy.is_file()):
            return "no copy"
        if (HashHandler.calculate_hash(origin) == 
                HashHandler.calculate_hash(copy)):
            return "same"
        else:
            return "different"

    def compare_hashes(self, origin: Path, copy: Path) -> bool:
        """
        Return True if hashes are the same
        Return False if hashes are different
        """
        # TODO: wrap exception
        return self.__json_handler.compare_hashes(origin, copy)

    def set_synclist(self, path: Path) -> None:
        """
        Set new sync list path
        """
        if not path:
            path: Path = Path(environ['HOME'] + r'/.config/filesync/synclist.json')
            if not path.exists():
                self.__create_file(path)
                with open(str(path), 'w') as f:
                    f.write('{}')

        # TODO: rewrite exceptions
        try:
            self.__json_handler = JsonHandler(path)
        except FileIsNotJsonError:
            print("error Handled")
        except Exception as e:
            print("Exception handled:", e)

    def exec(request):
        res = exec(f"{request['method']}({request['data']})")
        return res

    def __set_origin_hash(self, origin: Path) -> None:
        """
        Set hash for origin
        """
        self.__json_handler.check_existing(origin)
        _hash: str = HashHandler.calculate_hash(origin)
        data: Dict[str, Any] = self.__json_handler.read()
        data[str(origin)]['hash'] = _hash
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

    def __update_copies(self) -> None:
        """
        Copy changed origins to all its copy
        """
        changed_origins: List[Path] = self.__json_handler.get_all_changed_origins()
        origin: Path
        copy: Path
        for origin in changed_origins:
            for copy in self.__json_handler.get_copies(origin):
                shutil_copy(str(origin), str(copy))

    def __create_file(self, path: Path):
        """
        Create file if it does not exsists
        """
        foldiers: Path = path.parent
        foldiers.mkdir(parents=True, exist_ok=True)
        path.touch()


def main() -> None:
    origin: Path = Path('file1.file').resolve()
    copy1: Path = Path('file2.file').resolve()
    copy2: Path = Path('file3.file').resolve()
    fs = FileSync()
    fs.add(origin, [copy1, copy2])
    fs.sync_all()
    # for o in fs.get_origins():
        # print(fs.get_copies(o))
    # print(fs.list_all())
    # print(type(origin))
    # print(origin)
    # print(fs.get_copies(origin))
    # print(str(origin))
    # fs.update_all_hashes()
    # fs.add(origin, copy)
    # fs.sync_two_files(origin, copy)
    # fs.full_sync()
    # fs.sync()

if __name__ == '__main__':
    main()
