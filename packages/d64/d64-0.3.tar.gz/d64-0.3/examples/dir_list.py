from d64 import DiskImage

with DiskImage('test/data/test.d64') as image:
    for line in image.directory():
        print(line)
