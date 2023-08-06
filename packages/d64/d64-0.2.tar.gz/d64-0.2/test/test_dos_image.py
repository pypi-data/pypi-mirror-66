import unittest

from d64.disk_image import D64Image

from test.mock_block import MockBlock


class TestDiskImageRead(unittest.TestCase):

    def setUp(self):
        self.dir_data = b'\x12\x01A\x00\x15\xff\xff\x1f\x15\xff\xff\x1f\x15\xff\xff\x1f\x15\xff\xff\x1f\x15\xff\xff\x1f\x15\xff\xff\x1f\x15\xff\xff\x1f\x04\x80\x02\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0el\xfb\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x02\x00\x12\xff\xff\x03\x12\xff\xff\x03\x12\xff\xff\x03\x12\xff\xff\x03\x11\xff\xff\x01\x11\xff\xff\x01\x11\xff\xff\x01\x11\xff\xff\x01\x11\xff\xff\x01GAMES TAPE\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0GT\xa02A\xa0\xa0\xa0\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.image = D64Image(None)
        self.image.dir_block = MockBlock()

    def test_read_dos_version(self):
        self.image.map = self.dir_data
        self.assertEqual(self.image.dos_version, ord('A'))

    def test_read_name(self):
        self.image.dir_block.data = self.dir_data
        self.assertEqual(self.image.name, b'GAMES TAPE')

    def test_read_id(self):
        self.image.dir_block.data = self.dir_data
        self.assertEqual(self.image.id, b'GT')

    def test_dos_type(self):
        self.image.dir_block.data = self.dir_data
        self.assertEqual(self.image.dos_type, b'2A')


class TestDiskImageWrite(unittest.TestCase):

    def setUp(self):
        self.image = D64Image(None)
        self.image.dir_block = MockBlock()

    def test_write_dos_version(self):
        self.image.map = bytearray(256)
        self.image.dos_version = 0x64
        self.assertEqual(self.image.dos_version, 0x64)

    def test_write_name(self):
        self.image.dir_block.data = bytearray(256)
        self.image.name = b'EXAMPLE'
        self.assertEqual(self.image.name, b'EXAMPLE')

    def test_write_id(self):
        self.image.dir_block.data = bytearray(256)
        self.image.id = b'EX'
        self.assertEqual(self.image.id, b'EX')

    def test_write_dos_type(self):
        self.image.dir_block.data = bytearray(256)
        self.image.dos_type = b'47'
        self.assertEqual(self.image.dos_type, b'47')
