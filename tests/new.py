from sys import path
path.insert(0, '../src/')
from pathlib import Path
from json_handler import JsonHandler


jh = JsonHandler(Path('testdata.json'))
jh.add_origin(Path("testfile1.file"))
jh.add_copy(Path("testfile1.file"), Path("testfile2.file"))
