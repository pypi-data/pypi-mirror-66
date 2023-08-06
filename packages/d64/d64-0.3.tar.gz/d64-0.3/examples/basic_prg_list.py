from d64 import DiskImage, ProgramFile

with DiskImage('test/data/test.d64') as image:
    with image.path("METEOR").open() as f:
        p = ProgramFile(f)

for line in p.list():
    print(line)
