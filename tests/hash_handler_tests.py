from sys import path
path.insert(0, '../src/')
from unittest import TestCase, main
from hash_handler import HashHandler


class HashHandlerTestCase(TestCase):
    """Tests for HashHandler"""

    def test_check_calculate_hash_sha1(self) -> str:
        hh = HashHandler()
        default_hash: str = '33ab5639bfd8e7b95eb1d8d0b87781d4ffea4d5d'
        _hash: str = hh.calculate_hash('testfile.file')

        self.assertEqual(default_hash, _hash)

if __name__ == '__main__':
    main()
