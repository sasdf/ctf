class PosRange(object):
    def __init__(self, start: int, stop=None):
        assert(isinstance(start, int))
        self.start = start
        if stop is None:
            stop = start + 1
        assert(stop > start)
        self.stop = stop

    def copy(self):
        return PosRange(self.start, self.stop)

    @property
    def det(self):
        return self.start + 1 == self.stop

    def __add__(self, other: int):
        return PosRange(self.start + other, self.stop + other)

    __radd__ = __add__

    def __sub__(self, other: int):
        return PosRange(self.start - other, self.stop - other)

    def __and__(self, other: 'PosRange'):
        start = max(self.start, other.start)
        stop = min(self.stop, other.stop)
        assert(start < stop)
        return PosRange(start, stop)

    __rand__ = __and__

    def __iand__(self, other: 'PosRange'):
        res = self & other
        self.start, self.stop = res.start, res.stop
        return self

    def __lt__(self, other: 'PosRange'):
        if self.start == other.start and self.stop == other.stop:
            return False
        elif self.start >= other.start and self.stop <= other.stop:
            return True
        elif other.start >= self.start and other.stop <= self.stop:
            return False
        else:
            return None

    def __repr__(self):
        return f'({self.start}, {self.stop})'
