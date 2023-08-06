import unittest

from d64 import DOSPath


class TestWildcards(unittest.TestCase):

    def test_wildcards(self):
        self.assertTrue(DOSPath.wildcard_match(b'EXACT', 'PRG', 'EXACT'))
        self.assertFalse(DOSPath.wildcard_match(b'EXYCT', 'PRG', 'EXACT'))
        self.assertFalse(DOSPath.wildcard_match(b'EXACTLY', 'PRG', 'EXACT'))
        self.assertFalse(DOSPath.wildcard_match(b'EXA', 'PRG', 'EXACT'))

        self.assertTrue(DOSPath.wildcard_match(b'SINGLE', 'PRG', 'SINGL?'))
        self.assertTrue(DOSPath.wildcard_match(b'SINGLE', 'PRG', '?INGLE'))
        self.assertFalse(DOSPath.wildcard_match(b'SINGLE', 'PRG', 'SINGLE?'))

        self.assertTrue(DOSPath.wildcard_match(b'MULTIPLE', 'PRG', 'MULTIPLE*'))
        self.assertTrue(DOSPath.wildcard_match(b'MULTIPLE', 'PRG', 'MULTIPL*'))
        self.assertTrue(DOSPath.wildcard_match(b'MULTIPLE', 'PRG', 'MULTIP*'))

        self.assertTrue(DOSPath.wildcard_match(b'TYPE', 'PRG', '*=PRG'))
        self.assertTrue(DOSPath.wildcard_match(b'TYPE', 'PRG', '*=P'))
        self.assertFalse(DOSPath.wildcard_match(b'TYPE', 'PRG', '*=S'))

        self.assertTrue(DOSPath.wildcard_match(b'TYPE', 'PRG', 'TYPE=PRG'))
        self.assertFalse(DOSPath.wildcard_match(b'TYPER', 'PRG', 'TYPE=PRG'))
        self.assertFalse(DOSPath.wildcard_match(b'TYPE', 'PRG', 'TYPE=SEQ'))
        self.assertTrue(DOSPath.wildcard_match(b'TYPE', 'PRG', 'TYPE*=PRG'))
        self.assertFalse(DOSPath.wildcard_match(b'TYPE', 'PRG', 'TYPE*=SEQ'))


if __name__ == '__main__':
    unittest.main()
