class Formatter(object):
    def __init__(self, path: str, format: str):
        self.path = path
        self.format = format
        self.raw_data = self.extract_data(format)

    def format(self):
        raise NotImplementedError
