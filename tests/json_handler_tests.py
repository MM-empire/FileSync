from sys import path
path.insert(0, '../src/')
from pathlib import Path
from unittest import TestCase, main
from json_handler import JsonHandler
from typing import Dict, Any, List

class JsonHandlerTestCase(TestCase):
    """Tests for JsonHandler"""


    def test_check_get_path(self):
        path: Path = Path('testdata.json')
        jh: JsonHandler = JsonHandler(path)
        self.assertEqual(path, jh.path)
    
    def test_check_read(self):
        path: Path = Path('testdata.json')
        jh: JsonHandler = JsonHandler(path)
        data: Dict[str, Any] = {'testfile1.file': {'hash': None, 'copies':
            {'testfile2.file': {'hash': None}}}}
        _data: Dict[str, Any] = jh.read()
        self.assertEqual(data, _data)

    def test_check_exists_origin(self):
        path: Path = Path('testdata.json')
        jh: JsonHandler = JsonHandler(path)
        testfile: Path = Path('testfile1.file')
        result: bool = jh.exists_origin(testfile)
        self.assertEqual(True, result)

    def test_check_exists_copy(self):
        path: Path = Path('testdata.json')
        jh: JsonHandler = JsonHandler(path)
        testfile1: Path = Path('testfile1.file')
        testfile2: Path = Path('testfile2.file')
        result: bool = jh.exists_copy(testfile1, testfile2)
        self.assertEqual(True, result)

    def test_check_get_origins(self):
        path: Path = Path('testdata.json')
        jh: JsonHandler = JsonHandler(path)
        testfile1: Path = Path('testfile1.file')
        origins: List[Path] = [testfile1]
        _origins: List[Path] = jh.get_origins()
        self.assertEqual(origins, _origins)


if __name__ == '__main__':
    main()
