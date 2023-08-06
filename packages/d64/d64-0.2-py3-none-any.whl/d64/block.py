import struct


class Block(object):
    """Storage block."""
    SECTOR_SIZE = 256

    def __init__(self, image, t, s):
        self.track = t
        self.sector = s
        self.start = image.block_start(t, s)
        self.image = image
        t, s = struct.unpack('<BB', self.image.map[self.start:self.start+2])
        self.next_track = t
        self.next_sector = s

    @property
    def data_size(self):
        if self.next_track:
            return self.SECTOR_SIZE-2
        return self.next_sector-1

    def next(self):
        """Return block linked from this one."""
        if self.next_track == 0:
            return None
        return Block(self.image, self.next_track, self.next_sector)

    def get(self, rel_start, rel_end):
        """Return a slice within this block."""
        return self.image.map[self.start+rel_start:self.start+rel_end]

    def set(self, rel_start, data):
        """Update a slice within this block."""
        if not self.image.writeable:
            raise PermissionError("Image is read-only")
        self.image.map[self.start+rel_start:self.start+rel_start+len(data)] = data
