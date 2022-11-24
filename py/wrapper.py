from typing import Any, Callable, Generic, TypeVar


T = TypeVar("T")
U = TypeVar("U")

class override:
    def __init__(self, cb: Callable):
        self.cb = cb
    def __call__(self, *args, **kwargs):
        self.cb(*args, **kwargs)
    def __str__(self):
        return f"{self.cb}"
    def __repr__(self):
        return f"<shadowed function {self.cb!r}>"
    def __get__(self, *args, **kwargs):
        return self.cb.__get__(*args, **kwargs)

class Wrapper(Generic[T]):
    def __init__(self, value: T):
        Wrapper._set_value(self, value)
    
    def __getattribute__(self, attr: str):
        try:
            o = object.__getattribute__(self, attr)
            if isinstance(o, override):
                return o
        except AttributeError:
            pass

        return getattr(Wrapper._value(self), attr)
    def __setattr__(self, __name: str, __value: Any) -> None:
        return setattr(Wrapper._value(self), __name, __value)
    def __delattr__(self, __name: str) -> None:
        return delattr(Wrapper._value(self), __name)
    
    def __str__(self):
        return str(Wrapper._value(self))
    def __repr__(self):
        return repr(Wrapper._value(self))
    
    def _value(self):
        return object.__getattribute__(self, "value")
    def _set_value(self, value: T):
        return object.__setattr__(self, "value", value)
    
    def __lt__(self, other):
        return Wrapper._value(self).__lt__(other)
    def __le__(self, other):
        return Wrapper._value(self).__le__(other)
    def __eq__(self, other):
        return Wrapper._value(self).__eq__(other)
    def __ne__(self, other):
        return Wrapper._value(self).__ne__(other)
    def __ge__(self, other):
        return Wrapper._value(self).__ge__(other)
    def __gt__(self, other):
        return Wrapper._value(self).__gt__(other)
    def __abs__(self):
        return Wrapper._value(self).__abs__()
    def __add__(self, other):
        return Wrapper._value(self).__add__(other)
    def __and__(self, other):
        return Wrapper._value(self).__and__(other)
    def __floordiv__(self, other):
        return Wrapper._value(self).__floordiv__(other)
    def __index__(self):
        return Wrapper._value(self).__index__()
    def __invert__(self):
        return Wrapper._value(self).__invert__()
    def __lshift__(self, other):
        return Wrapper._value(self).__lshift__(other)
    def __mod__(self, other):
        return Wrapper._value(self).__mod__(other)
    def __mul__(self, other):
        return Wrapper._value(self).__mul__(other)
    def __matmul__(self, other):
        return Wrapper._value(self).__matmul__(other)
    def __neg__(self):
        return Wrapper._value(self).__neg__()
    def __or__(self, other):
        return Wrapper._value(self).__or__(other)
    def __pos__(self):
        return Wrapper._value(self).__pos__()
    def __pow__(self, other, modulo=None):
        return Wrapper._value(self).__pow__(other, modulo)
    def __rshift__(self, other):
        return Wrapper._value(self).__rshift__(other)
    def __sub__(self, other):
        return Wrapper._value(self).__sub__(other)
    def __truediv__(self, other):
        return Wrapper._value(self).__truediv__(other)
    def __xor__(self, other):
        return Wrapper._value(self).__xor__(other)
    def __concat__(self, other):
        return Wrapper._value(self).__concat__(other)
    def __contains__(self, other):
        return Wrapper._value(self).__contains__(other)
    def __delitem__(self, other):
        return Wrapper._value(self).__delitem__(other)
    def __getitem__(self, other):
        return Wrapper._value(self).__getitem__(other)
    def __setitem__(self, other, value):
        return Wrapper._value(self).__setitem__(other, value)
    def __call__(self, *args, **kwargs):
        return Wrapper._value(self).__call__(*args, **kwargs)
    
    def _class(self):
        return object.__getattribute__(self, "__class__")
    def map(self, cb: Callable[[T], U]) -> "Wrapper[U]":
        return Wrapper._class(self)(cb(Wrapper._value(self)))
    
class Unwrap(Wrapper):
    def __getattribute__(self, attr: str):
        return object.__getattribute__(object.__getattribute__(self, "value"), attr)