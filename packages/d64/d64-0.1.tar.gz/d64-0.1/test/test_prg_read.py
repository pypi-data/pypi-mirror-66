import hashlib
import unittest

from d64 import DiskImage


class TestPrgRead(unittest.TestCase):

    def test_read_entry(self):
        csum = hashlib.md5()
        with DiskImage('test/data/test.d64') as image:
            with image.path("METEOR").open() as f:
                # read less than remaining in block
                data = f.read(100)
                csum.update(data)
                self.assertEqual(len(data), 100)
                # read to end of block
                data = f.read(154)
                csum.update(data)
                self.assertEqual(len(data), 154)
                # read multiple blocks
                data = f.read(643)
                csum.update(data)
                self.assertEqual(len(data), 643)
                # read remaining data
                data = f.read(240)
                csum.update(data)
                self.assertEqual(len(data), 100)
                # attempt to read beyond EOF
                data = f.read(20)
                self.assertEqual(len(data), 0)

        self.assertEqual(csum.hexdigest(), 'a008430c0b6eafeede397bc6a6ba6656')


if __name__ == '__main__':
    unittest.main()
