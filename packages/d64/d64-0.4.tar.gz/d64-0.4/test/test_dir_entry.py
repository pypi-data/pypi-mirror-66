import unittest
from unittest.mock import Mock

from d64.dir_entry import DirEntry


class TestDirEntryRead(unittest.TestCase):

    def test_read_prg(self):
        image = Mock()
        image.map = b'\x00\x00\x82\x0A\x14\x46\x49\x47\x48\x54\x45\x52\x20\x52\x41\x49\x44\xA0\xA0\xA0\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xE7\x01'
        ent = DirEntry(image, 0)
        self.assertEqual(ent.file_type, 'PRG')
        self.assertEqual(ent.protected, False)
        self.assertEqual(ent.closed, True)
        self.assertEqual(ent.start_ts, (10, 20))
        self.assertEqual(ent.name, b'FIGHTER RAID')
        self.assertEqual(ent.size, 487)

    def test_read_seq(self):
        image = Mock()
        image.map = b'\x00\x00\x81\x0A\x14\x46\x49\x47\x48\x54\x45\x52\x20\x52\x41\x49\x44\xA0\xA0\xA0\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xE7\x01'
        ent = DirEntry(image, 0)
        self.assertEqual(ent.file_type, 'SEQ')
        self.assertEqual(ent.protected, False)
        self.assertEqual(ent.closed, True)

        image.map = b'\x00\x00\x41\x0A\x14\x46\x49\x47\x48\x54\x45\x52\x20\x52\x41\x49\x44\xA0\xA0\xA0\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xE7\x01'
        ent = DirEntry(image, 0)
        self.assertEqual(ent.file_type, 'SEQ')
        self.assertEqual(ent.protected, True)
        self.assertEqual(ent.closed, False)

    def test_read_usr(self):
        image = Mock()
        image.map = b'\x00\x00\x83\x0A\x14\x46\x49\x47\x48\x54\x45\x52\x20\x52\x41\x49\x44\xA0\xA0\xA0\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xE7\x01'
        ent = DirEntry(image, 0)
        self.assertEqual(ent.file_type, 'USR')
        self.assertEqual(ent.protected, False)
        self.assertEqual(ent.closed, True)

        image.map = b'\x00\x00\x43\x0A\x14\x46\x49\x47\x48\x54\x45\x52\x20\x52\x41\x49\x44\xA0\xA0\xA0\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xE7\x01'
        ent = DirEntry(image, 0)
        self.assertEqual(ent.file_type, 'USR')
        self.assertEqual(ent.protected, True)
        self.assertEqual(ent.closed, False)

    def test_read_rel(self):
        image = Mock()
        image.map = b'\x00\x00\x84\x0A\x14\x46\x49\x47\x48\x54\x45\x52\x20\x52\x41\x49\x44\xA0\xA0\xA0\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xE7\x01'
        ent = DirEntry(image, 0)
        self.assertEqual(ent.file_type, 'REL')


class TestDirEntryWrite(unittest.TestCase):

    def test_write_file_type(self):
        image = Mock()
        image.map = bytearray(32)
        ent = DirEntry(image, 0)
        ent.file_type = 'prg'
        self.assertEqual(image.map[2], 0x82)
        ent.file_type = 0x43
        self.assertEqual(image.map[2], 0x43)

    def test_write_protected(self):
        image = Mock()
        image.map = bytearray(32)
        ent = DirEntry(image, 0)
        ent.file_type = 0x82
        ent.protected = True
        self.assertEqual(image.map[2], 0xc2)

    def test_write_closed(self):
        image = Mock()
        image.map = bytearray(32)
        ent = DirEntry(image, 0)
        ent.file_type = 0xc2
        ent.closed = False
        self.assertEqual(image.map[2], 0x42)

    def test_write_start_ts(self):
        image = Mock()
        image.map = bytearray(32)
        ent = DirEntry(image, 0)
        ent.start_ts = (21, 11)
        self.assertEqual(image.map[3:5], b'\x15\x0b')

    def test_write_name(self):
        image = Mock()
        image.map = bytearray(32)
        ent = DirEntry(image, 0)
        ent.name = b'NIBBLERS'
        self.assertEqual(image.map[5:21], b'NIBBLERS\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0')

    def test_write_size(self):
        image = Mock()
        image.map = bytearray(32)
        ent = DirEntry(image, 0)
        ent.size = 1234
        self.assertEqual(image.map[0x1e:0x20], b'\xd2\x04')
