from sys import path
import os
from pathlib import Path
from typing import List
from unittest import TestCase, main

path.insert(0, "../../src/")
from file_sync import FileSync
from hash_handler import HashHandler
#from HashHandler import calculate_hash


class TestFileSync(TestCase):
    """Test for FileSync"""

    def setUp(self):
        self.origin: Path = Path("file1.file")
        self.copies: List[Path] = [Path("output_dir/file1.file")]
        self.synclist: Path = Path("synclist.json")

        # remove old files
        try:
            os.remove(self.origin)
            for copy in self.copies:
                os.remove(copy)
            os.remove(self.synclist)
        except Exception:
            pass

        # create file
        with open(self.origin, "w") as f:
            f.write("Hello World!")

    def test_check_sync(self):
        """Test if sync single file works fine"""
        fs = FileSync(path=self.synclist)
        fs.add(self.origin, self.copies)
        fs.sync(self.origin)
        for copy in self.copies:
            self.assertEqual(HashHandler.calculate_hash(self.origin),
                             HashHandler.calculate_hash(copy))


if __name__ == "__main__":
    main()
