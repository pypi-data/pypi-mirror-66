from contextlib import contextmanager

from .block import Block
from .file import File


class DOSPath(object):
    """Encapsulate a path within an image."""
    def __init__(self, image, entry=None):
        self.image = image
        self.entry = entry
        self.block = None

    def __str__(self):
        return self.entry.name.decode()

    @property
    def size_blocks(self):
        """Return file size in blocks."""
        return self.entry.size

    @property
    def size_bytes(self):
        """Return file size in bytes."""
        size = 0

        block = Block(self.image, *self.entry.start_ts)
        while block:
            size += block.data_size
            block = block.next_block()

        return size

    @contextmanager
    def open(self, mode='r'):
        """Return new file object."""
        f = File(self.entry, mode)
        yield f

    def iterdir(self, include_deleted=False):
        """Iterate over a path."""
        for entry in self.image.dir_entries():
            if include_deleted or entry._file_type() != 0:
                yield DOSPath(self.image, entry)

    def glob(self, pattern, include_deleted=False):
        """Return paths that match a wildcard pattern."""
        for path in self.iterdir(include_deleted):
            if self.wildcard_match(path.entry.name, path.entry.file_type, pattern):
                yield path

    @staticmethod
    def wildcard_match(fname, ftype, wildcard):
        """Return True if file matches a DOS wildcard."""

        if isinstance(wildcard, str):
            wildcard = wildcard.encode()

        if b'=' in wildcard:
            # file type
            if wildcard[-1] == ord('='):
                raise ValueError("Invalid wildcard, "+wildcard)
            wildcard, wftype = wildcard.split(b'=', 1)
            if ord(ftype[0]) != wftype[0]:
                return False

        for w, f in zip(wildcard, fname):
            if w == ord('?'):
                # matches any character
                continue
            if w == ord('*'):
                # matches rest of file name
                return True
            if w != f:
                return False

        if len(fname)+1 == len(wildcard) and wildcard.endswith(b'*'):
            # zero length match
            return True
        return len(fname) == len(wildcard)
