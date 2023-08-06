import unittest

from d64 import DiskImage


class TestDirRead(unittest.TestCase):

    def test_read_entry(self):
        with DiskImage('test/data/test.d64') as image:
            e = image.path("CATACOMBS")
            self.assertEqual(e.size_blocks, 16)
            self.assertEqual(e.size_bytes, 3813)

    def test_iter(self):
        with DiskImage('test/data/test.d64') as image:
            p = image.path()
            entries = [e for e in p.iterdir()]
            self.assertEqual(len(entries), 28)
            entries = [e for e in p.iterdir(include_deleted=True)]
            self.assertEqual(len(entries), 29)
            entries = [e for e in p.glob("T*")]
            self.assertEqual(len(entries), 3)
            entries = [e for e in p.glob("T*", include_deleted=True)]
            self.assertEqual(len(entries), 4)
            entries = [e for e in p.glob("*=S")]
            self.assertEqual(len(entries), 1)


if __name__ == '__main__':
    unittest.main()
