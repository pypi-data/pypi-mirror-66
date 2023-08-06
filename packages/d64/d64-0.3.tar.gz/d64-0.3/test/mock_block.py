class MockBlock(object):
    def __init__(self):
        self.data = b''
        self.start = 0

    def get(self, start, end):
        return self.data[start:end]

    def set(self, start, new):
        self.data[start:start+len(new)] = new
