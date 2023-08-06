from pathlib import Path
import itertools


class Iterable:
    def __init__(self, iterable):
        self.iterable = list(iterable)
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index == len(self.iterable):
            self.index = -1
            raise StopIteration
        return self.iterable[self.index]

    def map(self, func):
        return Iterable(map(func, self.iterable))

    def filter(self, func):
        return Iterable(filter(func, self.iterable))

    def __str__(self):
        return str(f"Iterable object!\nself.iterable: {self.iterable}")

    def flatten_once(self):
        try:
            self.iterable = list(itertools.chain.from_iterable(self.iterable))
        except TypeError:
            raise TypeError("Elements of the iterable are not iterable! Can't flatten them.")
        return self


class FolderIterable(Iterable):
    def __init__(self, path):
        self.iterable = list(Path(path).glob("*"))
        self.index = -1

    def __str__(self):
        return str(f"FolderIterable object!\nself.iterable: {self.iterable}")


def expand_dir(dir):
    return list(Path(dir).glob("*"))
