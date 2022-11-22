#!/usr/bin/env python3
from sys import path
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any
from unittest import TestCase, main

path.insert(0, "../../src/")
from fs_core import FileSync
from json_handler import JsonHandler
from hash_handler import HashHandler
from exceptions import OriginDoesNotExistsError


class TestFileSync(TestCase):
    """Test FileSync"""

    def create_file(self, path: Path, msg: str = "Hello World!") -> None:
        msg = f"{str(path)} {msg}"
        foldiers: Path = path.parent
        foldiers.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(msg)

    def setUp(self):
        # change dir to test_dir
        self.test_dir_path: Path = Path("test_dir")
        os.makedirs(self.test_dir_path)
        os.chdir(self.test_dir_path)

        self.origin: Path = Path("file1.file")
        self.copies: List[Path] = [Path("output_dir/file1.file")]
        self.synclist: Path = Path("synclist.json")

        self.create_file(self.origin)

        self.fs = FileSync(path=self.synclist)

    def tearDown(self):
        os.chdir("..")
        shutil.rmtree(self.test_dir_path)

    def test_add(self):
        """Test add"""
        self.fs.add(self.origin, self.copies)

        self.assertEqual([self.origin.resolve()], self.fs.get_origins())
        self.assertEqual([copy.resolve() for copy in self.copies],
                         self.fs.get_copies(self.origin))

    def test_add_origin(self):
        """Test add origin"""
        self.fs.add_origin(self.origin)
        self.assertEqual([self.origin.resolve()], self.fs.get_origins())

    def test_sync(self):
        """Test sync"""
        self.fs.add(self.origin, self.copies)
        self.fs.sync(self.origin)
        for copy in self.copies:
            self.assertEqual(HashHandler.calculate_hash(self.origin),
                             HashHandler.calculate_hash(copy))

    def test_sync_all(self):
        """Test sync_all"""
        new_file: Path = Path("copy_file2.file")
        self.create_file(new_file, msg="other content")
        self.copies.append(new_file)
        self.copies.append(Path("copy_file3.file"))

        new_origin: Path = Path("new_origin")
        self.create_file(new_origin, msg="origin content")
        new_copy1: Path = Path("new_copy1")
        new_copy2: Path = Path("new_copy2")
        new_copy3: Path = Path("new_copy3")
        new_copies: List[Path] = [new_copy1, new_copy2, new_copy3]

        self.fs.add(self.origin, self.copies)
        self.fs.add(new_origin, new_copies)
        self.fs.update_all_hashes()
        self.fs.sync_all()

        for copy in self.copies:
            self.assertEqual(HashHandler.calculate_hash(self.origin),
                             HashHandler.calculate_hash(copy))

        for copy in new_copies:
            self.assertEqual(HashHandler.calculate_hash(new_origin),
                             HashHandler.calculate_hash(copy))

    def test_delete(self):
        """Test delete"""
        self.fs.add(self.origin, self.copies)
        self.fs.sync(self.origin)
        self.fs.delete(self.origin.resolve())

        try:
            self.fs.get_copies(self.origin)
        except OriginDoesNotExistsError:
            pass
        except Exception as e:
            self.fail(e)

    def test_get_origins(self):
        """Test get_origins"""
        origin: Path = Path("file2.file")
        copy: Path = Path("copy_file2.file")
        self.create_file(origin)

        self.fs.add(self.origin, self.copies)
        self.fs.add(origin, [copy])

        self.assertEqual([self.origin.resolve(), origin.resolve()], self.fs.get_origins())

    def test_get_copies(self):
        """Test get_copies"""
        self.copies.append(Path("copy_file2.file"))
        self.copies.append(Path("copy_file3.file"))

        self.fs.add(self.origin, self.copies)

        self.assertEqual([copy.resolve() for copy in self.copies], self.fs.get_copies(self.origin))

        syncList_new: Path = Path("synclist_new.json")
        fs_new = FileSync(syncList_new)

        try:
            fs_new.get_copies(self.origin)
        except OriginDoesNotExistsError:
            pass
        except Exception as e:
            self.fail(e)

    def test_get_copy_status(self):
        """Test get_copy_status"""
        self.fs.add(self.origin, self.copies)
        copy: Path = self.copies[0]
        self.assertEqual("no copy", self.fs.get_copy_status(self.origin, copy))

        self.create_file(copy)
        self.assertEqual("different", self.fs.get_copy_status(self.origin, copy))

        self.fs.sync(self.origin)
        self.assertEqual("same", self.fs.get_copy_status(self.origin, copy))

    # def test_compare_hashes(self):
    #     """Test compare_hashes"""
    #     new_file: Path = Path("new_file.file")
    #     # self.create_file(new_file, msg="other content")
    #     self.fs.add(self.origin, [new_file])
    #     self.fs.sync(self.origin)
    #
    #     print("origins:", self.fs.get_origins())
    #     print("copies:", self.fs.get_copies(self.origin))
    #
    #     self.assertTrue(self.fs.compare_hashes(self.origin, self.copies))
        # self.assertFalse(self.fs.compare_hashes(self.origin, new_file))

    def test_set_synclist(self):
        """Test set_synclist"""
        synclist_new: Path = Path("new_synclist.json")
        self.fs.add(self.origin, self.copies)
        self.fs.set_synclist(synclist_new)
        self.fs.add(self.origin, self.copies)

        self.assertEqual(HashHandler.calculate_hash(self.synclist.resolve()),
                         HashHandler.calculate_hash(synclist_new.resolve()))

    def test_set_origin_hash(self):
        """Test __set_origin_hash"""
        self.fs.add(self.origin, self.copies)
        os.remove(self.origin)
        self.create_file(self.origin, "new content")

        jh = JsonHandler(self.synclist)
        data: Dict[str, Any] = jh.read()

        self.assertNotEqual(data[str(self.origin.resolve())]['hash'],
                         HashHandler.calculate_hash(self.origin))

        self.fs._FileSync__set_origin_hash(self.origin.resolve())

        data: Dict[str, Any] = jh.read()
        self.assertEqual(data[str(self.origin.resolve())]['hash'],
                         HashHandler.calculate_hash(self.origin))

    def test_set_copy_hash(self):
        """Test __set_copy_hash"""
        self.fs.add(self.origin, self.copies)
        self.fs.sync(self.origin)

        jh = JsonHandler(self.synclist)
        data: Dict[str, Any] = jh.read()
        for copy in self.copies:
            self.assertEqual(data[str(self.origin.resolve())]['copies'][str(copy.resolve())]['hash'],
                             HashHandler.calculate_hash(copy.resolve()))

        for copy in self.copies:
            os.remove(copy)
            self.create_file(copy, "new content")

        for copy in self.copies:
            self.assertNotEqual(data[str(self.origin.resolve())]['copies'][str(copy.resolve())]['hash'],
                             HashHandler.calculate_hash(copy.resolve()))

        for copy in self.copies:
            self.fs._FileSync__set_copy_hash(self.origin.resolve(), copy.resolve())

        data: Dict[str, Any] = jh.read()
        for copy in self.copies:
            self.assertEqual(data[str(self.origin.resolve())]['copies'][str(copy.resolve())]['hash'],
                             HashHandler.calculate_hash(copy.resolve()))

    def test_create_file(self):
        """Test __create_file"""
        file_path: Path = Path("create.file")
        self.fs._FileSync__create_file(file_path)
        self.assertTrue(file_path.exists())

    def test_create_file_recursive(self):
        """Test __create_file recursive"""
        full_path: Path = Path("folder/subfolder/create.file")
        self.fs._FileSync__create_file(full_path)
        self.assertTrue(Path(full_path).resolve().exists())


if __name__ == "__main__":
    main()
