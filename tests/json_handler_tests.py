from sys import path
from json import dump 
path.insert(0, '../src/')
from pathlib import Path
from unittest import TestCase, main
from json_handler import JsonHandler
from typing import Dict, Any, List
from os import system


class JsonHandlerTestCase(TestCase):
    """Tests for JsonHandler"""

    @classmethod
    def setUpClass(cls):
        cls.path: Path = Path('testfiles/testdata.json')
        cls.jh: JsonHandler = JsonHandler(cls.path)
        cls.testfile1: Path = Path('testfiles/testfile1.file')
        cls.testfile2: Path = Path('testfiles/testfile2.file')

        with open(cls.path, 'w') as f:
            data: Dict[str, Any] = {'testfiles/testfile1.file': {'hash': None, 'copies':
                {'testfiles/testfile2.file': {'hash': None}}}}
            dump(data, f, indent=4);

    @classmethod
    def tearDownClass(cls):
        system(f'rm {cls.path}')

    def test_check_get_path(self):
        self.assertEqual(self.path, self.jh.path)
    
    def test_check_read(self):
        data: Dict[str, Any] = {'testfiles/testfile1.file': {'hash': None, 'copies':
            {'testfiles/testfile2.file': {'hash': None}}}}
        _data: Dict[str, Any] = self.jh.read()
        self.assertEqual(data, _data)

    def test_check_exists_origin(self):
        result: bool = self.jh.exists_origin(self.testfile1)
        self.assertEqual(True, result)

    def test_check_exists_copy(self):
        result: bool = self.jh.exists_copy(self.testfile1, self.testfile2)
        self.assertEqual(True, result)

    def test_check_get_origins(self):
        origins: List[Path] = [self.testfile1]
        _origins: List[Path] = self.jh.get_origins()
        self.assertEqual(origins, _origins)

    def test_check_get_copies(self):
        copies: List[Path] = [self.testfile2]
        _copies: List[Path] = self.jh.get_copies(self.testfile1)
        self.assertEqual(copies, _copies)


if __name__ == '__main__':
    main()
