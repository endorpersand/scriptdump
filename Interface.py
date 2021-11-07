"""
creation: February 16, 2021
rewritten: November 7, 2021

Implementation of very simple interfaces (inspired by TS) in Python

"""

import functools
import inspect
from abc import ABCMeta
from collections.abc import Set, Mapping
from typing import Callable

class _InterfaceMeta(ABCMeta):
    def __new__(meta, clsname, bases, attrs, *, name = None, props=None):
        # save all required properties to cls._props
        if props is None:
            props = frozenset()
        else:
            props = frozenset(props)
        
        for B in bases:
            if meta.is_interface(B):
                props |= B.props
        
        attrs["_props"] = props

        # check if it has a given name (only for Interface types, not subclasses of interfaces)
        attrs["_has_name"] = name is not None
        if name is None: name = clsname
        
        # interface specific methods (not subclasses of interfaces)

        # add hooked __init__ and __delattr__ to bypass subclass override
        _delattr = attrs.get("__delattr__", None)
        def __delattr__(self, name):
            if name not in self.__class__.props:
                if _delattr is not None: return _delattr(self, name)
                else: return super(self.__class__, self).__delattr__(name)
            raise TypeError(f"Cannot delete interface property {repr(name)}")
        attrs["__delattr__"] = __delattr__
        
        _init = attrs.get("__init__", None)
        def __init__(self, *args, **kwargs):
            if _init is not None: _init(self, *args, **kwargs)
            else: return super(self.__class__, self).__init__(*args, **kwargs)
            
            for prop in props:
                # prop exists in instance's __dict__ or some class's __dict__
                if prop not in self.__dict__ and not any(prop in B.__dict__ for B in self.__class__.__mro__): 
                    raise NameError(f"Missing property '{prop}'")
        
        if _init is not None: __init__.__signature__ = inspect.signature(_init)
        attrs["__init__"] = __init__

        # init class
        return super().__new__(
            meta, name, bases, attrs
        )
    
    @staticmethod
    def is_interface(C):
        return C.__class__ is _InterfaceMeta and \
               not any(B.__class__ is _InterfaceMeta for B in C.__mro__[1:])

    @property
    def props(cls):
        return cls._props

    def _reprname(cls, using_brackets=True):
        if cls._has_name: return cls.__name__

        copy = set(cls.props)

        if using_brackets:
            if len(copy) == 0: return "{}"
            else: return repr(copy)
        else:
            return f"Interface({repr(copy)})"
        
    def __repr__(cls):
        if cls.is_interface(cls):
            return f"<interface {cls._reprname()}>"
        return super().__repr__()

    def __and__(cls, other):
        if not cls.is_interface(cls) or not cls.is_interface(other): return super().__and__(other)
        return Interface(cls.props | other.props)

    def __or__(cls, other):
        if not cls.is_interface(cls) or not cls.is_interface(other): return super().__or__(other)
        return Interface(cls.props & other.props)

def Interface(required_props: Set | Callable[[], Set]):
    if callable(required_props):
        iface_name = required_props.__name__
        props = required_props()
    else:
        iface_name = None
        props = required_props
    
    class _interface(metaclass=_InterfaceMeta, name=iface_name, props=props):
        def __init__(self, *args, **kwargs):
            if self.__class__ is _interface:
                if len(args) > 0: dct = args[0]
                else: dct = {}

                if len(dct) != 0:
                    if isinstance(dct, Mapping): self.__dict__.update(dct)
                    else: self.__dict__.update(enumerate(dct))
                if len(kwargs) != 0: self.__dict__.update(kwargs)
            else:
                super().__init__(*args, **kwargs)

        def __getitem__(self, item):
            if item in self.__class__.props:
                return self.__dict__[item]
            raise TypeError(f"{item} is not part of the interface")
        
        @classmethod
        def __subclasshook__(cls, C):
            if cls is _interface:
                # check that every property exists somewhere in one of the classes of the object's MRO
                return all(any(prop in B.__dict__ for B in C.__mro__) for prop in cls.props)
            return NotImplemented
        
        def __repr__(self):
            if self.__class__ is _interface:
                return f"{self.__class__._reprname(False)}({repr(self.__dict__)})"
            return super().__repr__()

    return _interface

@Interface
def Box(): return {"values"}

@Interface
def Boolean(): return {"truth"}

def SizedList(n): 

    @Interface
    def Sized(): return set(range(0, n))
    Sized.__name__ = f"SizedList{n}"

    return Sized

@Interface
def Thinker(): return {"think", "values"}

def smart_intersect(*interfaces):
    c = functools.reduce(lambda a, b: a | b, interfaces)
    c.resolve = lambda self: next((i for i in interfaces if isinstance(self, i)), Interface(set()))
    return c