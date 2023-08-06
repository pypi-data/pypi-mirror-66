# d64

This Python module enables access to disk image files (.d64) used by various Commodore microcomputer emulators and tools.

It provides familiar interfaces for developers to read (and eventually write) program and data files within an image.


## Examples

Classes and functions reside in the `d64` module, the whole module may be imported or just those definitions referenced by the user.

### Displaying an image contents

To perform a directory list

```python
from d64 import DiskImage

with DiskImage('test/data/squadron.d64') as image:
    for line in image.directory():
        print(line)
```

This prints out

```
0 "SQUADRON        " Q9 2A
15   "SQUADRON PAL"     PRG
15   "SQUADRON NTSC"    PRG
634 BLOCKS FREE.
```

### Listing a BASIC program

To display a BASIC program as text

```python
from d64 import DiskImage, ProgramFile

with DiskImage('test/data/test.d64') as image:
    with image.path("METEOR").open() as f:
        p = ProgramFile(f)

for line in p.list():
    print(line)
```


## TODO

- interactive shell utility
- support .d71
- support .d81
- better docstrings
- more examples
- File write support
- Entry deletion
- Empty image creation
- codec support (use [cbmcodecs](https://pypi.org/project/cbmcodecs/))
