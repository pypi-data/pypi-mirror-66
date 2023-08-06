import os
import os.path
import shutil
import tempfile

from .bam import D64BAM
from .block import Block
from .dos_image import DOSImage


class D64Image(DOSImage):

    MAX_TRACK = 35
    DIR_TRACK = 18
    INTERLEAVE = 10
    DIR_INTERLEAVE = 3
    TRACK_SECTOR_MAX = ((21, (1, 17)), (19, (18, 24)), (18, (25, 30)), (17, (31, 35)))

    def __init__(self, filename):
        self.bam = D64BAM(self)
        super().__init__(filename)

    def alloc_first_block(self):
        """Allocate the first block for a new file."""
        track = None
        for low, high in zip(range(self.DIR_TRACK-1, 0, -1), range(self.DIR_TRACK+1, self.MAX_TRACK+1)):
            total, free_bits = self.bam.get_entry(low)
            if total:
                track = low
                break
            total, free_bits = self.bam.get_entry(high)
            if total:
                track = high
                break

        if track is None:
            # tried either side of the directory, disk is full
            return None
        sector = self.bam.free_from(free_bits, 0)

        self.bam.set_allocated(track, sector)
        return Block(self, track, sector)

    def alloc_next_block(self, track, sector, interleave):
        """Allocate a subsequent block for a file."""
        cur_track = track
        cur_sector = sector
        delta = -1 if track < self.DIR_TRACK else 1
        tries = 2  # either side of directory track

        while True:
            total, free_bits = self.bam.get_entry(cur_track)
            if total:
                # free sector in current track
                cur_sector += interleave
                if cur_sector >= self.max_sectors(cur_track):
                    cur_sector -= self.max_sectors(cur_track)
                    if cur_sector:
                        cur_sector -= 1

                cur_sector = self.bam.free_from(free_bits, cur_sector)
                self.bam.set_allocated(cur_track, cur_sector)
                return Block(self, cur_track, cur_sector)

            if cur_track == self.DIR_TRACK:
                # tried either side of the directory then the directory, disk is full
                return None

            cur_track += delta
            if cur_track == 0 or cur_track > self.MAX_TRACK:
                # end of disk
                cur_sector = 0
                tries -= 1
                if tries:
                    # try other side of directory
                    delta = -delta
                    cur_track = self.DIR_TRACK + delta
                else:
                    # tried either side of the directory, try directory track
                    cur_track = self.DIR_TRACK


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
