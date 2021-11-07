
def singleton(cls):
    st = cls()
    def __new__(*args): return st
    cls.__new__ = __new__
    return st

@singleton
class Universe:
    def __contains__(self, n): return True
    def __iter__(self): return self
    def __next__(self): return self
    def __getattribute__(self, name): return self
    def __setattr__(self, name, value): return
    def __delattr__(self, name: str): pass
    def __call__(self, *args, **kwargs): return self

import collections.abc

class CollectionMap(collections.abc.Iterator):
    def __new__(cls, mapper, col):
        if not isinstance(col, collections.abc.Collection): 
            raise TypeError("Cannot create mapped collection with a non-collection")
        
        o = super().__new__(cls)
        o.iter = map(mapper, col)
        o.col = col
        return o
    
    def __next__(self): return next(self.iter)
    def __len__(self): return len(self.col)
    def __contains__(self, i): return i in self.iter

class chain:
    def __init__(self, f):
        self.f = f
        self.args = []
        self.kwargs = {}
    
    def __call__(self, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0: return self.f(*self.args, **self.kwargs)

        self.args.extend(args)
        self.kwargs.update(kwargs)

        return self

class Noneish:
    def __init__(self, v):
        if isinstance(v, Noneish):
            self.v = v.v
        else:
            self.v = v

    @property
    def __none(self):
        return Noneish(None)

    def __str__(self):
        return f"{self.v}?"

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.v)})"

    def __getattr__(self, attr):
        if self.v == None: return self.__none
        return Noneish(getattr(self.v, attr))
    
    def __call__(self, *args, **kwargs):
        if self.v == None: return self.__none
        return Noneish(self.v(*args, **kwargs))

    def __getitem__(self, a):
        if self.v == None: return self.__none
        return Noneish(self.v[a])

dehex = lambda it: (int(''.join(tp),16) for tp in it)

def chunk(iterable, n):
    from itertools import zip_longest
    it = iter(iterable)
    return zip_longest(*[it]*n)