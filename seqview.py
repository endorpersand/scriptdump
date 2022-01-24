"""
Jan 13, 2022
"""

from collections.abc import MutableSequence
from typing import Generic, SupportsIndex, TypeVar

T = TypeVar("T")

class MutSeqView(Generic[T], MutableSequence[T]):

    def __init__(self, seq: MutableSequence[T], start: int = None, stop: int = None, step: int = None):
        self.seq = seq
        self.slice = slice(start, stop, step)

    @classmethod
    def from_slice(cls, seq: MutableSequence[T], slic: slice):
        return cls(seq, *slic.indices(len(seq)))

    @staticmethod
    def _merge(length: int, s1: "slice | SupportsIndex", s2: "slice | SupportsIndex"):
        if not isinstance(s1, slice):
            s1 = slice(s1, s1 + 1)
        if not isinstance(s2, slice):
            s2 = slice(s2, s2 + 1)

        r = range(length)[s1][s2]
        return slice(r.start, r.stop, r.step)

    @property
    def _sli(self):
        return self.slice.indices(len(self.seq))
    
    @property
    def _slice_range(self):
        return range(*self._sli)

    def __getitem__(self, i):
        ns = self._merge(len(self.seq), self.slice, i)
        return self.__class__.from_slice(self.seq, ns)

    def __setitem__(self, k, v):
        ns = range(len(self.seq))[self.slice][k]

        return self.seq.__setitem__(ns, v)

    def __delitem__(self, i):
        ns = self._merge(len(self.seq), self.slice, i)
        return self.seq.__delitem__(ns)

    def __len__(self):
        return len(self._slice_range)

    def insert(self, k, v):
        raise TypeError("Cannot insert on view")

    def __repr__(self):
        return f"#{list(self.seq[self.slice])!r}"