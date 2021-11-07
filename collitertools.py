from collections.abc import *
import itertools
import operator

from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    SupportsComplex,
    SupportsFloat,
    SupportsInt,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

T = TypeVar("T")
S = TypeVar("S")
N = TypeVar("N", int, float, SupportsFloat, SupportsInt, SupportsComplex)
Step = Union[int, float, SupportsFloat, SupportsInt, SupportsComplex]

class count(Iterable[N], Container[N], Generic[N]):
    def __init__(self, start: N = 0, step: N = 1):
        self.start = start
        self.step = step

    def __iter__(self) -> Iterator[N]:
        return itertools.count(self.start, self.step)
    
    def __contains__(self, other: N) -> bool:
        if self.step == 0:
            return other == self.start
        d, m = divmod(other - self.start, self.step)
        return m == 0 and d >= 0
    
    def __repr__(self):
        step = ""
        if not isinstance(step, int) or step != 1:
            step = ", " + repr(self.step)
        return "{}({})"\
            .format(self.__class__.__qualname__,
                    repr(self.start),
                    step)
    
class cycle(Iterable[T], Container[T], Generic[T]):
    def __init__(self, coll: Collection[T]):
        self.coll = coll
    
    def __iter__(self) -> Iterator[T]:
        while True:
            yield from self.coll
    
    def __contains__(self, other: T) -> bool:
        return other in self.coll


class repeat_infinite(Iterable[T], Container[T], Generic[T]):
    def __init__(self, o: T):
        self.o = o

    def __iter__(self) -> Iterator[T]:
        return itertools.repeat(self.o)

    def __contains__(self, other: T):
        return other == self.o
    
    def __repr__(self):
        return "{}({})".format(repeat.__qualname__, repr(self.o))

class repeat(Collection[T], Generic[T]):
    def __new__(cls, o: T, times: int = None):
        if times is None: return repeat_infinite(o)
        return super().__new__(cls)

    def __init__(self, o: T, times: int = None):
        self.o = o
        self.times = times
    
    def __iter__(self) -> Iterator[T]:
        return itertools.repeat(self.o, self.times)

    def __contains__(self, other: T):
        return other == self.o

    def __len__(self):
        return self.times

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__qualname__, repr(self.o), repr(self.times))

class accumulate(Collection[T], Generic[T]):
    def __init__(self, collection: Collection[T], func: Callable[[T, T], T] = operator.add, *, initial: T | None = None):
        self.collection = collection
        self.func = func
        self.initial = initial

    def __iter__(self) -> Iterator[T]:
        return itertools.accumulate(self.collection, self.func, initial=self.initial)
    
    def __contains__(self, other: T):
        return any(e == other for e in self)

    def __len__(self):
        return (self.initial is not None) + len(self.collection)

class chain(Collection[T], Generic[T]):
    def __init__(self, *colls: Collection[T]):
        self.colls: Iterable[Collection[T]] = colls

    @classmethod
    def from_iterable(cls, colls: "Iterable[Collection[T]]") -> "chain[T]":
        o = cls()
        o.colls = colls
        return o

    def _colls_iter(self):
        if hasattr(self, "_collsc"):
            yield from self._collsc
        else:
            self._collsc = []
            for c in self.colls:
                self._collsc.append(c)
                yield c

    def __iter__(self) -> Iterator[T]:
        for c in self._colls_iter():
            yield from c

    def __contains__(self, other: T):
        return any(other in c for c in self._colls_iter())

    def __len__(self):
        return sum(len(c) for c in self._colls_iter())

# class compress(Iterator[_T], Generic[_T]):
#     def __init__(self, data: Iterable[_T], selectors: Iterable[Any]) -> None: ...
#     def __iter__(self) -> Iterator[_T]: ...
#     def __next__(self) -> _T: ...

# class dropwhile(Iterator[_T], Generic[_T]):
#     def __init__(self, __predicate: Predicate[_T], __iterable: Iterable[_T]) -> None: ...
#     def __iter__(self) -> Iterator[_T]: ...
#     def __next__(self) -> _T: ...

# class filterfalse(Iterator[_T], Generic[_T]):
#     def __init__(self, __predicate: Predicate[_T] | None, __iterable: Iterable[_T]) -> None: ...
#     def __iter__(self) -> Iterator[_T]: ...
#     def __next__(self) -> _T: ...

# _T1 = TypeVar("_T1")
# _T2 = TypeVar("_T2")

# class groupby(Iterator[Tuple[_T, Iterator[_S]]], Generic[_T, _S]):
#     @overload
#     def __new__(cls, iterable: Iterable[_T1], key: None = ...) -> groupby[_T1, _T1]: ...
#     @overload
#     def __new__(cls, iterable: Iterable[_T1], key: Callable[[_T1], _T2]) -> groupby[_T2, _T1]: ...
#     def __iter__(self) -> Iterator[Tuple[_T, Iterator[_S]]]: ...
#     def __next__(self) -> Tuple[_T, Iterator[_S]]: ...

# class islice(Iterator[_T], Generic[_T]):
#     @overload
#     def __init__(self, __iterable: Iterable[_T], __stop: int | None) -> None: ...
#     @overload
#     def __init__(self, __iterable: Iterable[_T], __start: int | None, __stop: int | None, __step: int | None = ...) -> None: ...
#     def __iter__(self) -> Iterator[_T]: ...
#     def __next__(self) -> _T: ...

# class starmap(Iterator[_T], Generic[_T]):
#     def __init__(self, __function: Callable[..., _T], __iterable: Iterable[Iterable[Any]]) -> None: ...
#     def __iter__(self) -> Iterator[_T]: ...
#     def __next__(self) -> _T: ...

# class takewhile(Iterator[_T], Generic[_T]):
#     def __init__(self, __predicate: Predicate[_T], __iterable: Iterable[_T]) -> None: ...
#     def __iter__(self) -> Iterator[_T]: ...
#     def __next__(self) -> _T: ...

# def tee(__iterable: Iterable[_T], __n: int = ...) -> Tuple[Iterator[_T], ...]: ...

# class zip_longest(Iterator[Any]):
#     def __init__(self, *p: Iterable[Any], fillvalue: Any = ...) -> None: ...
#     def __iter__(self) -> Iterator[Any]: ...
#     def __next__(self) -> Any: ...

# _T3 = TypeVar("_T3")
# _T4 = TypeVar("_T4")
# _T5 = TypeVar("_T5")
# _T6 = TypeVar("_T6")

# class product(Iterator[_T_co], Generic[_T_co]):
#     @overload
#     def __new__(cls, __iter1: Iterable[_T1]) -> product[Tuple[_T1]]: ...
#     @overload
#     def __new__(cls, __iter1: Iterable[_T1], __iter2: Iterable[_T2]) -> product[Tuple[_T1, _T2]]: ...
#     @overload
#     def __new__(cls, __iter1: Iterable[_T1], __iter2: Iterable[_T2], __iter3: Iterable[_T3]) -> product[Tuple[_T1, _T2, _T3]]: ...
#     @overload
#     def __new__(
#         cls, __iter1: Iterable[_T1], __iter2: Iterable[_T2], __iter3: Iterable[_T3], __iter4: Iterable[_T4]
#     ) -> product[Tuple[_T1, _T2, _T3, _T4]]: ...
#     @overload
#     def __new__(
#         cls,
#         __iter1: Iterable[_T1],
#         __iter2: Iterable[_T2],
#         __iter3: Iterable[_T3],
#         __iter4: Iterable[_T4],
#         __iter5: Iterable[_T5],
#     ) -> product[Tuple[_T1, _T2, _T3, _T4, _T5]]: ...
#     @overload
#     def __new__(
#         cls,
#         __iter1: Iterable[_T1],
#         __iter2: Iterable[_T2],
#         __iter3: Iterable[_T3],
#         __iter4: Iterable[_T4],
#         __iter5: Iterable[_T5],
#         __iter6: Iterable[_T6],
#     ) -> product[Tuple[_T1, _T2, _T3, _T4, _T5, _T6]]: ...
#     @overload
#     def __new__(
#         cls,
#         __iter1: Iterable[Any],
#         __iter2: Iterable[Any],
#         __iter3: Iterable[Any],
#         __iter4: Iterable[Any],
#         __iter5: Iterable[Any],
#         __iter6: Iterable[Any],
#         __iter7: Iterable[Any],
#         *iterables: Iterable[Any],
#     ) -> product[Tuple[Any, ...]]: ...
#     @overload
#     def __new__(cls, *iterables: Iterable[_T1], repeat: int) -> product[Tuple[_T1, ...]]: ...
#     @overload
#     def __new__(cls, *iterables: Iterable[Any], repeat: int = ...) -> product[Tuple[Any, ...]]: ...
#     def __iter__(self) -> Iterator[_T_co]: ...
#     def __next__(self) -> _T_co: ...

# class permutations(Iterator[Tuple[_T, ...]], Generic[_T]):
#     def __init__(self, iterable: Iterable[_T], r: int | None = ...) -> None: ...
#     def __iter__(self) -> Iterator[Tuple[_T, ...]]: ...
#     def __next__(self) -> Tuple[_T, ...]: ...

# class combinations(Iterator[_T_co], Generic[_T_co]):
#     @overload
#     def __new__(cls, iterable: Iterable[_T], r: Literal[2]) -> combinations[Tuple[_T, _T]]: ...
#     @overload
#     def __new__(cls, iterable: Iterable[_T], r: Literal[3]) -> combinations[Tuple[_T, _T, _T]]: ...
#     @overload
#     def __new__(cls, iterable: Iterable[_T], r: Literal[4]) -> combinations[Tuple[_T, _T, _T, _T]]: ...
#     @overload
#     def __new__(cls, iterable: Iterable[_T], r: Literal[5]) -> combinations[Tuple[_T, _T, _T, _T, _T]]: ...
#     @overload
#     def __new__(cls, iterable: Iterable[_T], r: int) -> combinations[Tuple[_T, ...]]: ...
#     def __iter__(self) -> Iterator[_T_co]: ...
#     def __next__(self) -> _T_co: ...

# class combinations_with_replacement(Iterator[Tuple[_T, ...]], Generic[_T]):
#     def __init__(self, iterable: Iterable[_T], r: int) -> None: ...
#     def __iter__(self) -> Iterator[Tuple[_T, ...]]: ...
#     def __next__(self) -> Tuple[_T, ...]: ...

# if sys.version_info >= (3, 10):
#     class pairwise(Iterator[_T_co], Generic[_T_co]):
#         def __new__(cls, __iterable: Iterable[_T]) -> pairwise[Tuple[_T, _T]]: ...
#         def __iter__(self) -> Iterator[_T_co]: ...
#         def __next__(self) -> _T_co: ...
