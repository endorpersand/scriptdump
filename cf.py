"""
Jan 23, 2022
"""

import operator
from typing import Callable

class ComposableFunction():
    def __init__(self, callback: Callable):
        if not callable(callback): raise TypeError("callback is not callable")
        self.c = callback
    
    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.c.__name__} at {hex(id(self))}>"

    def __call__(self, *args, **kwargs):
        res = self.c(*args, **kwargs)
        
        if callable(res):
            return ComposableFunction(res)
        return res
    
    @staticmethod
    def _get_cb(f):
        if isinstance(f, ComposableFunction):
            return f.c
        elif callable(f):
            return f
        return None

    @staticmethod
    def _compose(f, g):
        def _(*args, **kwargs): return f(g(*args, **kwargs))
        return ComposableFunction(_)

    @staticmethod
    def _merge_fs(o, *fs):
        def _(*args, **kwargs): return o(*(f(*args, **kwargs) for f in fs))
        return ComposableFunction(_)

    def _apply(self, o, *args):
        cbs = [self._get_cb(a) for a in args]

        if all(c is not None for c in cbs):
            return self._merge_fs(o, self.c, *cbs)
        return NotImplemented
    
    def _rapply(self, o, *args):
        cbs = [self._get_cb(a) for a in args]

        if len(cbs) == 0:
            return self._merge_fs(o, self.c)
        if all(c is not None for c in cbs):
            return self._merge_fs(o, cbs[0], self.c, *cbs[1:])
        return NotImplemented

    def __add__(self, o): return self._apply(operator.add, o)
    def __sub__(self, o): return self._apply(operator.sub, o)
    def __mul__(self, o): return self._apply(operator.mul, o)
    def __floordiv__(self, o): return self._apply(operator.floordiv, o)
    def __truediv__(self, o): return self._apply(operator.truediv, o)
    def __mod__(self, o): return self._apply(operator.mod, o)
    def __matmul__(self, o): 
        if (cb := self._get_cb(o)) is not None:
            return self._compose(self, cb)
        return NotImplemented
    def __pow__(self, o, m = lambda: None): return self._apply(pow, o, m)

    def __abs__(self): return self._apply(operator.abs)
    def __index__(self): return self._apply(operator.index)
    def __invert__(self): return self._apply(operator.invert)
    def __neg__(self): return self._apply(operator.neg)
    def __pos__(self): return self._apply(operator.pos)

    def __and__(self, o): return self._apply(operator.and_, o)
    def __or__(self, o): return self._apply(operator.or_, o)
    def __xor__(self, o): return self._apply(operator.xor, o)
    def __lshift__(self, o): return self._apply(operator.lshift, o)
    def __rshift__(self, o): return self._apply(operator.rshift, o)

    def __radd__(self, o): return self._rapply(operator.add, o)
    def __rsub__(self, o): return self._rapply(operator.sub, o)
    def __rmul__(self, o): return self._rapply(operator.mul, o)
    def __rfloordiv__(self, o): return self._rapply(operator.floordiv, o)
    def __rtruediv__(self, o): return self._rapply(operator.truediv, o)
    def __rmod__(self, o): return self._rapply(operator.mod, o)
    def __rmatmul__(self, o): 
        if (cb := self._get_cb(o)) is not None:
            return self._compose(cb, self)
        return NotImplemented
    def __rpow__(self, o, m = lambda: None): return self._rapply(operator.pow, o, m)

    def __rand__(self, o): return self._rapply(operator.and_, o)
    def __ror__(self, o): return self._rapply(operator.or_, o)
    def __rxor__(self, o): return self._rapply(operator.xor, o)
    def __rlshift__(self, o): return self._rapply(operator.lshift, o)
    def __rrshift__(self, o): return self._rapply(operator.rshift, o)

cf = ComposableFunction
