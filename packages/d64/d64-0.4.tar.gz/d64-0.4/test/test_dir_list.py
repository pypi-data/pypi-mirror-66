import unittest

from d64 import DiskImage


class TestDirList(unittest.TestCase):

    def test_dir_list(self):
        txt = ''
        with DiskImage('test/data/test.d64') as image:
            for line in image.directory():
                txt += line + '\n'
        ref = '''0 "GAMES TAPE      " GT 2A
10   "TANK-V-UFO"       PRG
4    "KILLER COMET"     PRG
5    "ROCKET COMMAND"   PRG
10   "RAINBOW PASSAGE"  PRG
9    "MINOTAUR"         PRG
4    "DEMON DRIVER"     PRG
4    "BRAMBLES"         PRG
9    "SIMON"            PRG
12   "DUCK SHOOT"       PRG
10   "NIBBLERS"         PRG
12   "DRAGON HUNTER"    PRG
5    "BREAKOUT"         PRG
11   "TANK BATTLE"      PRG
4    "FIGHTER RAID"     PRG<
4    "METEOR"           PRG
8    "MARS REVENGE"    *PRG
14   "SALVAGE DIVER"    PRG
8    "SPACE RUNNER"     PRG
16   "CATACOMBS"        PRG
6    "BOMBER"           PRG
10   "PAC-MAN"          PRG
1    "DATA"             SEQ
1    "DATAWRITE"        PRG
33   "JELLY MONSTERS"   PRG
1    "DATAREAD"         PRG
1    "LOADER"           PRG
66   "THE COUNT"        PRG
69   "POPEYE2015"       PRG
309 BLOCKS FREE.
'''
        self.assertEqual(txt, ref)


if __name__ == '__main__':
    unittest.main()
