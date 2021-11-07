from collections import defaultdict
from typing import Generic, TypeVar, Callable

T = TypeVar("T")
U = TypeVar("U")

class Optional(Generic[T]):
    def __init__(self, obj: "Optional[T]" | T | None):
        self.obj: T | None
        if isinstance(obj, Optional):
            self.obj = obj.obj
        else:
            self.obj = obj

    @classmethod
    def some(cls, obj: T):
        if obj is None: raise ValueError(f"object is None")
        return cls(obj)
        
    def is_some(self):
        return self.obj is not None

    def is_none(self):
        return self.obj is None

    def __and__(self, other: "Optional[U]") -> "Optional[U]":
        if self.is_none(): return Optional.none
        return other
    
    def __or__(self, other: "Optional[U]"):
        if self.is_some(): return self
        return other
    
    def and_then(self, func: "Callable[[T], Optional[U]]") -> "Optional[U]":
        if self.is_none(): return Optional.is_none
        return func(self.obj)

    def or_else(self, func: "Callable[[], Optional[U]]") -> "Optional[U]":
        if self.is_some(): return self
        return func()

    def __xor__(self, other: "Optional[U]"):
        is_some = self.is_some() ^ other.is_some()

        if not is_some: return Optional.none
        if self.is_some(): return self
        return other

    def __call__(self, *args, **kwargs):
        if self.is_none(): return self
        return Optional(self.obj(*args, **kwargs))

    def filter(self, pred: Callable[[T], bool]) -> "Optional[T]":
        if self.is_none(): return Optional.none
        if not pred(self.obj): return Optional.none
        return self

    def map(self, func: Callable[[T], U]) -> "Optional[U]":
        if self.is_none(): return Optional.is_none
        return self.__class__(func(self.obj))

    MISSING = object()
    def get(self, *, or_else=MISSING):
        MISSING = self.MISSING

        if self.is_none():
            if or_else is MISSING: raise ValueError(f"object is None")
            return or_else
        return self.obj

    def __iter__(self):
        if self.is_some(): yield self.obj

    def __eq__(self, other):
        return self.obj == other.obj

    def __repr__(self) -> str:
        qualname = self.__class__.__qualname__
        if self.is_none(): return f"{qualname}.none"
        return f"{qualname}({self.obj})"

Optional.none = Optional(None)