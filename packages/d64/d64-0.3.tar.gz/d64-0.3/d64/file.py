from .block import Block


class File(object):
    """Read and write access to files."""
    def __init__(self, entry, mode):
        self.image = entry.image
        self.entry = entry
        self.mode = mode
        self.block = Block(self.image, *self.entry.start_ts)
        self.pos_block = 2

    def read(self, count=-1):
        """Read bytes from file."""
        ret = b''

        while count:
            remaining = self.block.data_size-(self.pos_block-2)
            if remaining == 0:
                break

            # read as much as is wanted from the current block
            length = remaining if count == -1 else min(count, remaining)
            ret += self.block.get(self.pos_block, self.pos_block+length)
            self.pos_block += length
            if count != -1:
                count -= length

            if self.block.is_final:
                # no more blocks, end of file
                break

            if self.pos_block == Block.SECTOR_SIZE:
                # end of block, move on to the next block
                self.block = self.block.next_block()
                self.pos_block = 2

        return ret
