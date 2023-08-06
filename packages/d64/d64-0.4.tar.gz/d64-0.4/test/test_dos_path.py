import unittest

from d64.dos_path import DOSPath


class TestDOSPath(unittest.TestCase):

    def test_open_read_exists(self):
        path = DOSPath(None, entry='x')
        with path.open('r') as file_:
            self.assertIsNotNone(file_)

    def test_open_read_exists(self):
        path = DOSPath(None, name='x')
        with self.assertRaises(FileNotFoundError):
            with path.open('r') as file_:
                pass


if __name__ == '__main__':
    unittest.main()
