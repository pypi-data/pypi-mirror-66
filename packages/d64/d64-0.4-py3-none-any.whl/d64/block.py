import struct


class Block(object):
    """Storage block."""
    SECTOR_SIZE = 256

    def __init__(self, image, track, sector):
        self.track = track
        self.sector = sector
        self.start = image.block_start(track, sector)
        self.image = image

    @property
    def is_final(self):
        """Return `True` if no next block."""
        return self.image.map[self.start] == 0

    @property
    def data_size(self):
        """Return the amount of data within this block."""
        if not self.is_final:
            return self.SECTOR_SIZE-2
        s = self.image.map[self.start+1]
        if s == 0:
            raise IndexError("Invalid data size")
        return s-1

    def next_block(self):
        """Return block linked from this one."""
        if self.is_final:
            return None
        t, s = struct.unpack('<BB', self.image.map[self.start:self.start+2])
        return Block(self.image, t, s)

    def get(self, rel_start, rel_end):
        """Return a slice of data within this block."""
        return self.image.map[self.start+rel_start:self.start+rel_end]

    def set(self, rel_start, data):
        """Update a slice of data within this block."""
        if not self.image.writeable:
            raise PermissionError("Image is read-only")
        self.image.map[self.start+rel_start:self.start+rel_start+len(data)] = data
