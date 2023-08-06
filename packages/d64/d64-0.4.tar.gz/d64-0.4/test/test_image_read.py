import mmap
import unittest

from d64.block import Block
from d64.disk_image import D64Image


class TestImageRead(unittest.TestCase):

    def test_read(self):
        image = D64Image('dummy.d64')
        image.map = mmap.mmap(-1, 174848)
        image.dir_block = Block(image, image.DIR_TRACK, 0)

        image.writeable = True
        image.dir_block.set(2, b'A')
        image.dir_block.set(0x90, b'TEST\xa0\xa0\xa0\xa0\xa0\xa0')
        image.dir_block.set(0xa2, b'ST')
        image.dir_block.set(0xa5, b'2A')
        image.writeable = False

        self.assertEqual(image.dos_version, ord('A'))
        self.assertEqual(image.name, b'TEST')
        self.assertEqual(image.id, b'ST')
        self.assertEqual(image.dos_type, b'2A')


if __name__ == '__main__':
    unittest.main()
