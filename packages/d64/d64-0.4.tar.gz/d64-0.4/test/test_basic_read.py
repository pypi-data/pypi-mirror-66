import io
import unittest

from d64.basic_file import BASICFile


class TestBASICRead(unittest.TestCase):

    def test_read_basic(self):
        data = b'\x14\x12\x0a\x00\x99\x22\x48\x45\x4c\x4c\x4f\x20\x57\x4f\x52\x4c\x44\x22\x00\x1d\x12\x14\x00\x89\x20\x31\x30\x00\x00\x00'
        buf = io.BytesIO(data)
        i = 0
        line_nums = (10, 20)
        line_tokens = (b'\x99"HELLO WORLD"', b'\x89 10')

        f = BASICFile(buf, 0x1201)
        for line in f.dump():
            self.assertEqual(line[0], line_nums[i])
            self.assertEqual(line[1], line_tokens[i])
            i += 1


if __name__ == '__main__':
    unittest.main()
