import dataclasses
from typing import Generic, TypeVar

T = TypeVar("T")

@dataclasses.dataclass
class Ref(Generic[T]):
    """
    Reference type, allows copy-by-ref mechanics for non-reference types
    """
    deref: T

    def __getitem__(self, t):
        if deshadow(t) in (slice(None), 0):
            return self.deref
        raise ValueError("Invalid deref")
    
    def __setitem__(self, t, value):
        if t in (slice(None), 0):
            self.deref = deshadow(value)
        else:
            raise ValueError("Invalid deref")
    
    def __getattr__(self, attr: str):
        return getattr(self.deref, deshadow(attr))
    
    def __iter__(self):
        return iter((self.deref,))
    
    @property
    def _shadow(self) -> "ShadowRef[T]":
        return ShadowRef(self)
    @_shadow.setter
    def _shadow(self, value):
        self.deref = deshadow(value)
    
    def __eq__(self, other):
        return self is other
    
    def __str__(self):
        return f"&{self.deref}"

def deshadow(o):
    if isinstance(o, ShadowRef):
        return o._ref.deref
    return o

@dataclasses.dataclass
class ShadowRef(Generic[T]):
    """
    More obscure reference. This type acts nearly identically to the inner type,
    and can be passed to functions which don't expect a Ref.
    """
    _ref: Ref[T]

    @property
    def __class__(self):
        return self._ref.deref.__class__
    def __str__(self):
        return str(self._ref.deref)
    def __repr__(self):
        return repr(self._ref.deref)
    def __getattr__(self, attr):
        return getattr(self._ref.deref, deshadow(attr))
    def __setattr__(self, attr, value):
        return super().__setattr__(deshadow(attr), deshadow(value))
    def __delattr__(self, attr):
        return super().__delattr__(deshadow(attr))
    def __call__(self, *args, **kwargs):
        return self._ref.deref.__call__(*args, **kwargs)
    def __len__(self):
        return self._ref.deref.__len__()
    def __getitem__(self, key):
        return self._ref.deref.__getitem__(deshadow(key))
    def __setitem__(self, key, value):
        return self._ref.deref.__setitem__(deshadow(key), deshadow(value))
    def __delitem__(self, key):
        return self._ref.deref.__delitem__(deshadow(key))
    def __missing__(self, key):
        return self._ref.deref.__missing__(deshadow(key))
    def __iter__(self):
        return self._ref.deref.__iter__()
    def __reversed__(self):
        return self._ref.deref.__reversed__()
    def __contains__(self, item):
        return self._ref.deref.__contains__(deshadow(item))
    def __add__(self, other):
        return self._ref.deref.__add__(deshadow(other))
    def __sub__(self, other):
        return self._ref.deref.__sub__(deshadow(other))
    def __mul__(self, other):
        return self._ref.deref.__mul__(deshadow(other))
    def __matmul__(self, other):
        return self._ref.deref.__matmul__(deshadow(other))
    def __truediv__(self, other):
        return self._ref.deref.__truediv__(deshadow(other))
    def __floordiv__(self, other):
        return self._ref.deref.__floordiv__(deshadow(other))
    def __mod__(self, other):
        return self._ref.deref.__mod__(deshadow(other))
    def __divmod__(self, other):
        return self._ref.deref.__divmod__(deshadow(other))
    def __pow__(self, other, modulo = None):
        return self._ref.deref.__pow__(deshadow(other), deshadow(modulo))
    def __lshift__(self, other):
        return self._ref.deref.__lshift__(deshadow(other))
    def __rshift__(self, other):
        return self._ref.deref.__rshift__(deshadow(other))
    def __and__(self, other):
        return self._ref.deref.__and__(deshadow(other))
    def __xor__(self, other):
        return self._ref.deref.__xor__(deshadow(other))
    def __or__(self, other):
        return self._ref.deref.__or__(deshadow(other))
    def __radd__(self, other):
        return self._ref.deref.__radd__(deshadow(other))
    def __rsub__(self, other):
        return self._ref.deref.__rsub__(deshadow(other))
    def __rmul__(self, other):
        return self._ref.deref.__rmul__(deshadow(other))
    def __rmatmul__(self, other):
        return self._ref.deref.__rmatmul__(deshadow(other))
    def __rtruediv__(self, other):
        return self._ref.deref.__rtruediv__(deshadow(other))
    def __rfloordiv__(self, other):
        return self._ref.deref.__rfloordiv__(deshadow(other))
    def __rmod__(self, other):
        return self._ref.deref.__rmod__(deshadow(other))
    def __rdivmod__(self, other):
        return self._ref.deref.__rdivmod__(deshadow(other))
    def __rpow__(self, other, modulo = None):
        return self._ref.deref.__rpow__(deshadow(other), deshadow(modulo))
    def __rlshift__(self, other):
        return self._ref.deref.__rlshift__(deshadow(other))
    def __rrshift__(self, other):
        return self._ref.deref.__rrshift__(deshadow(other))
    def __rand__(self, other):
        return self._ref.deref.__rand__(deshadow(other))
    def __rxor__(self, other):
        return self._ref.deref.__rxor__(deshadow(other))
    def __ror__(self, other):
        return self._ref.deref.__ror__(deshadow(other))
    def __iadd__(self, other):
        self._ref.deref = (self._ref.deref.__iadd__ if hasattr(self._ref.deref, "__iadd__") else self._ref.deref.__add__)(deshadow(other))
        return self
    def __isub__(self, other):
        self._ref.deref = (self._ref.deref.__isub__ if hasattr(self._ref.deref, "__isub__") else self._ref.deref.__sub__)(deshadow(other))
        return self
    def __imul__(self, other):
        self._ref.deref = (self._ref.deref.__imul__ if hasattr(self._ref.deref, "__imul__") else self._ref.deref.__mul__)(deshadow(other))
        return self
    def __imatmul__(self, other):
        self._ref.deref = (self._ref.deref.__imatmul__ if hasattr(self._ref.deref, "__imatmul__") else self._ref.deref.__matmul__)(deshadow(other))
        return self
    def __itruediv__(self, other):
        self._ref.deref = (self._ref.deref.__itruediv__ if hasattr(self._ref.deref, "__itruediv__") else self._ref.deref.__truediv__)(deshadow(other))
        return self
    def __ifloordiv__(self, other):
        self._ref.deref = (self._ref.deref.__ifloordiv__ if hasattr(self._ref.deref, "__ifloordiv__") else self._ref.deref.__floordiv__)(deshadow(other))
        return self
    def __imod__(self, other):
        self._ref.deref = (self._ref.deref.__imod__ if hasattr(self._ref.deref, "__imod__") else self._ref.deref.__mod__)(deshadow(other))
        return self
    def __ipow__(self, other, modulo = None):
        self._ref.deref = (self._ref.deref.__ipow__ if hasattr(self._ref.deref, "__ipow__") else self._ref.deref.__pow__)(deshadow(other), deshadow(modulo))
        return self
    def __ilshift__(self, other):
        self._ref.deref = (self._ref.deref.__ilshift__ if hasattr(self._ref.deref, "__ilshift__") else self._ref.deref.__lshift__)(deshadow(other))
        return self
    def __irshift__(self, other):
        self._ref.deref = (self._ref.deref.__irshift__ if hasattr(self._ref.deref, "__irshift__") else self._ref.deref.__rshift__)(deshadow(other))
        return self
    def __iand__(self, other):
        self._ref.deref = (self._ref.deref.__iand__ if hasattr(self._ref.deref, "__iand__") else self._ref.deref.__and__)(deshadow(other))
        return self
    def __ixor__(self, other):
        self._ref.deref = (self._ref.deref.__ixor__ if hasattr(self._ref.deref, "__ixor__") else self._ref.deref.__xor__)(deshadow(other))
        return self
    def __ior__(self, other):
        self._ref.deref = (self._ref.deref.__ior__ if hasattr(self._ref.deref, "__ior__") else self._ref.deref.__or__)(deshadow(other))
        return self
    def __neg__(self):
        return self._ref.deref.__neg__()
    def __pos__(self):
        return self._ref.deref.__pos__()
    def __abs__(self):
        return self._ref.deref.__abs__()
    def __invert__(self):
        return self._ref.deref.__invert__()
    def __complex__(self):
        return self._ref.deref.__complex__()
    def __int__(self):
        return self._ref.deref.__int__()
    def __float__(self):
        return self._ref.deref.__float__()
    def __index__(self):
        return self._ref.deref.__index__()
    def __round__(self, ndigits = None):
        return self._ref.deref.__round__(deshadow(ndigits))
    def __trunc__(self):
        return self._ref.deref.__trunc__()
    def __floor__(self):
        return self._ref.deref.__floor__()
    def __ceil__(self):
        return self._ref.deref.__ceil__()
    def __bytes__(self):
        return self._ref.deref.__bytes__()
    def __format__(self, format_spec):
        return self._ref.deref.__format__(deshadow(format_spec))
    def __lt__(self, other):
        return self._ref.deref.__lt__(deshadow(other))
    def __le__(self, other):
        return self._ref.deref.__le__(deshadow(other))
    def __eq__(self, other):
        return self._ref.deref.__eq__(deshadow(other))
    def __ne__(self, other):
        return self._ref.deref.__ne__(deshadow(other))
    def __gt__(self, other):
        return self._ref.deref.__gt__(deshadow(other))
    def __ge__(self, other):
        return self._ref.deref.__ge__(deshadow(other))
    def __hash__(self):
        return self._ref.deref.__hash__()
    def __bool__(self):
        return self._ref.deref.__bool__()