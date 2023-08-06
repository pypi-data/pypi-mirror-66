import mmap
import os
import os.path
import shutil
import tempfile

from .bam import D64BAM
from .block import Block
from .dir_entry import DirEntry
from .dos_path import DOSPath


class DOSImage(object):
    def __init__(self, filename):
        self.filename = filename
        self.root_path = DOSPath(self)

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
        self.dir_block = Block(self, self.dir_track, 0)

    def close(self):
        self.map.close()
        self.fileh.close()

    def path(self, name=None):
        if name:
            if isinstance(name, str):
                name = name.encode()
            paths = [e for e in self.root_path.glob(name)]
            if paths:
                return paths[0]
            raise FileNotFoundError("File not found: "+name)

        # root directory
        return self.root_path

    def block_start(self, track, sector):
        if track == 0 or track > self.max_track:
            raise ValueError("Invalid track, %d" % track)

        sector_start = 0
        for sectors, track_range in self.track_sector_max:
            if track > track_range[1]:
                sector_start += (track_range[1]-track_range[0]+1) * sectors
            else:
                if sector >= sectors:
                    raise ValueError("Invalid sector, %d:%d" % (track, sector))
                sector_start += (track-track_range[0]) * sectors
                sector_start += sector
                break

        return sector_start*Block.SECTOR_SIZE

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
        block = Block(self, self.dir_track, 1)

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


class D64Image(DOSImage):
    def __init__(self, filename):
        self.max_track = 35
        self.dir_track = 18
        self.bam_offset = 4
        self.bam_entry_size = 4
        self.track_sector_max = ((21, (1, 17)), (19, (18, 24)), (18, (25, 30)), (17, (31, 35)))
        self.bam = D64BAM(self)
        super().__init__(filename)


class DiskImage(object):
    raw_modes = {'r': 'rb', 'w': 'r+b'}

    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = self.raw_modes.get(mode, 'rb')

    def __enter__(self):
        if self.mode == 'r+b':
            self.org_filename = self.filename
            tempf = tempfile.NamedTemporaryFile(prefix='d64-', dir=os.path.dirname(self.filename),
                                                delete=False)
            # copy existing file to temporary
            with open(self.org_filename, 'rb') as inh:
                shutil.copyfileobj(inh, tempf)
            tempf.close()
            self.filename = tempf.name

        self.image = D64Image(self.filename)
        self.image.open(self.mode)
        return self.image

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.image.close()

        if self.mode == 'r+b':
            if exc_type is None:
                # update original with modified file
                os.replace(self.filename, self.org_filename)
            else:
                os.remove(self.filename)
