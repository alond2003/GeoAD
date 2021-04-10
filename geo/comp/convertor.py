"""geo/comp/convertor.py"""


class Convertor:
    def __init__(self, tolist, get):
        self.tolist = tolist
        self.get = get

    def __getitem__(self, key):
        return [self.get(i) for i in self.tolist(key)]
