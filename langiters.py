"""
Jan 30, 2022
"""

from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Iterator, Iterable, MutableSequence, MutableSet, Sequence
from dataclasses import dataclass
from typing import Callable, Generic, MutableMapping, TypeVar

T = TypeVar("T")

class BoxedIterator(Generic[T], Iterator[T]):
    def __init__(self, it: Iterable[T]):
        self.it = iter(it)

    def __next__(self):
        """
        Next value if the object were treated as a Python iterator
        """
        return next(self.it)

class LangIterator(BoxedIterator[T], ABC):
    def __init__(self, it: Iterable[T]):
        super().__init__(it)

    @abstractmethod
    def _internal_next(self):
        """
        Internal next value, handles internals of how iterator is dealt with
        """
        return next(self.it)

    @abstractmethod
    def next(self):
        """
        Next value if the object were treated as an iterator from its source language
        """
        return self._internal_next()
    
    def __next__(self):
        """
        Next value if the object were treated as a Python iterator
        """
        return self.next()

class JavaIterator(LangIterator[T]):
    MISSING = object()

    def __init__(self, it: Iterable[T]):
        super().__init__(it)

        if isinstance(it, MutableSequence):
            self.oit = it
            self.ty = 1
            self.it = enumerate(tuple(it))
            self.removed_curr = False
            self.removed = 0
        elif isinstance(it, (MutableSet, MutableMapping)):
            self.oit = it
            self.ty = 2
            self.it = iter(frozenset(it))
        else:
            self.ty = 0
        
        self.cursor = deque([JavaIterator.MISSING, JavaIterator.MISSING], 2) # [current, future]
    
    def _internal_next(self, advance=True):
        MISSING = JavaIterator.MISSING

        # evaluate future
        if self.cursor[1] is MISSING:
            self.cursor[1] = super()._internal_next()

        # progress cursor if told to advance
        if advance:
            self.cursor.append(MISSING)
            if self.ty == 1: self.removed_curr = False
        
        return self.cursor[0]

    def has_next(self):
        try:
            self._internal_next(advance=False)
        except StopIteration:
            return False
        return True
    
    def next(self):
        n = self._internal_next()
        if self.ty == 1:
            return n[1]
        return n
        
    def remove(self):
        current = self.cursor[0]

        if current is JavaIterator.MISSING:
            raise ValueError("Nothing to remove")
        if self.ty == 2:
            if isinstance(self.oit, MutableSet):
                self.oit.remove(self.cursor[0])
            else:
                self.oit.pop(self.cursor[0])
        elif self.ty == 1:
            if self.removed_curr: raise ValueError("Nothing to remove")
            self.oit.pop(self.cursor[0][0] - self.removed)
            self.removed_curr = True
            self.removed += 1
        else:
            raise TypeError("This iterator does not support remove")
    
    def for_each_remaining(self, act: Callable[[T], None]):
        for e in self.it: act(e)

class JavaListIterator(Generic[T], Iterator[T]):
    def __init__(self, it: Sequence[T]):
        self.seq = it
        self.mutable = isinstance(it, MutableSequence)
        self.cursor = -1
        self.removed_here = False
    
    def add(self, e: T): 
        if not self.mutable: raise TypeError("This iterator does not support add")
        s: MutableSequence = self.seq
        self.cursor += 1
        s.insert(self.cursor, e)

    def has_next(self): return 0 <= self.next_index < len(self.seq)

    def has_previous(self): return 0 <= self.previous_index < len(self.seq)

    def next(self):
        self.removed_here = False
        value = self.seq[self.next_index()]
        self.cursor += 1
        return value

    def next_index(self): 
        return self.cursor + 1

    def previous(self):
        if self.previous_index() == -1: raise IndexError("list index out of range")
        self.removed_here = False
        value = self.seq[self.previous_index()]
        self.cursor -= 1
        return value

    def previous_index(self): 
        return self.cursor

    def remove(self): 
        if not self.mutable: raise TypeError("This iterator does not support remove")
        if self.removed_here: raise ValueError("Nothing to remove")
        del self.seq[self.cursor]
        self.removed_here = True

    def set(self, e: T): 
        if not self.mutable: raise TypeError("This iterator does not support set")
        if self.removed_here: raise ValueError("Cannot set at removed position")
        self.seq[self.cursor] = e
        
    def __next__(self):
        return self.next()

class JSIterator(LangIterator[T]):
    MISSING = object()

    @dataclass
    class IterReturn(Generic[T]):
        value: T
        done: bool

    def __init__(self, it: Iterable[T], final=None):
        super().__init__(it)
        self.final = final
    
    def _internal_next(self):
        return super()._internal_next()
    
    def next(self):
        try:
            n = super()._internal_next()
            return JSIterator.IterReturn(value=n, done=False)
        except StopIteration:
            return JSIterator.IterReturn(value=self.final, done=True)
    
    def __next__(self):
        return self._internal_next()

class IEnumerator(BoxedIterator[T]):
    UNINITIALIZED = object()
    DONE = object()

    def __init__(self, it: Iterable[T]):
        super().__init__(it)
        self._current = IEnumerator.UNINITIALIZED
        self.oit = it
        self.resettable = isinstance(self.it, Sequence)
    
    @property
    def current(self):
        if self._current is IEnumerator.UNINITIALIZED: raise ValueError('No value')
        elif self._current is IEnumerator.DONE: raise StopIteration

        return self._current

    def move_next(self):
        try:
            self._current = next(self.it)
            return True
        except StopIteration:
            self._current = IEnumerator.DONE
            return False

    def reset(self):
        if not self.resettable: raise TypeError("This enumerator does not support reset")
        self.it = iter(self.oit)
    
    def __next__(self):
        self.move_next()
        return self.current

