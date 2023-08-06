import mmap

from .block import Block
from .dir_entry import DirEntry
from .dos_path import DOSPath


class DOSImage(object):
    def __init__(self, filename):
        self.filename = filename
        self.root_path = DOSPath(self, name='<root>')

    def directory(self, drive=0):
        yield '{} "{:16}" {} {}'.format(drive, self.name.decode(), self.id.decode(), self.dos_type.decode())
        for path in self.root_path.iterdir():
            closed_ch = ' ' if path.entry.closed else '*'
            file_type = path.entry.file_type
            if path.entry.protected:
                file_type += '<'
            yield '{:5}{:18}{}{}'.format(str(path.size_blocks), '"'+str(path)+'"', closed_ch, file_type)
        yield '{} BLOCKS FREE.'.format(self.bam.total_free())

    def open(self, mode):
        self.fileh = open(self.filename, mode)
        self.writeable = mode == 'r+b'
        access = mmap.ACCESS_WRITE if self.writeable else mmap.ACCESS_READ
        self.map = mmap.mmap(self.fileh.fileno(), 0, access=access)
        self.dir_block = Block(self, self.DIR_TRACK, 0)

    def close(self):
        self.map.close()
        self.fileh.close()

    def path(self, name=None):
        if name:
            if isinstance(name, str):
                name = name.encode()
            paths = [e for e in self.root_path.glob(name)]
            if paths:
                # existing path
                return paths[0]
            return DOSPath(self, name=name)

        # root directory
        return self.root_path

    def block_start(self, track, sector):
        if track == 0 or track > self.MAX_TRACK:
            raise ValueError("Invalid track, %d" % track)

        sector_start = 0
        for sectors, track_range in self.TRACK_SECTOR_MAX:
            if track > track_range[1]:
                sector_start += (track_range[1]-track_range[0]+1) * sectors
            else:
                if sector >= sectors:
                    raise ValueError("Invalid sector, %d:%d" % (track, sector))
                sector_start += (track-track_range[0]) * sectors
                sector_start += sector
                break

        return sector_start*Block.SECTOR_SIZE

    def max_sectors(self, track):
        """Return the maximum sectors for a given track."""
        if track < 1:
            raise ValueError("Invalid track, %d" % track)

        for sectors, track_range in self.TRACK_SECTOR_MAX:
            if track <= track_range[1]:
                return sectors

        raise ValueError("Invalid track, %d" % track)

    @property
    def dos_version(self):
        ver = self.map[self.dir_block.start+2]
        return ver

    @property
    def name(self):
        name = self.dir_block.get(0x90, 0x9a)
        return name.rstrip(b'\xa0')

    @property
    def id(self):
        id = self.dir_block.get(0xa2, 0xa4)
        return id

    @property
    def dos_type(self):
        dos = self.dir_block.get(0xa5, 0xa7)
        return dos

    def dir_entries(self):
        block = Block(self, self.DIR_TRACK, 1)

        while block:
            for offset in range(0, 0x100, 0x20):
                if self.map[block.start+offset+3] != 0:
                    yield DirEntry(self, block.start+offset)

            block = block.next_block()

    @dos_version.setter
    def dos_version(self, version):
        self.map[self.dir_block.start+2] = version

    @name.setter
    def name(self, nam):
        self.dir_block.set(0x90, nam.ljust(16, b'\xa0'))

    @id.setter
    def id(self, id_):
        self.dir_block.set(0xa2, id_)

    @dos_type.setter
    def dos_type(self, dtype):
        self.dir_block.set(0xa5, dtype)
