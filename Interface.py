from abc import ABCMeta
import functools

class InterfaceMeta(ABCMeta):

    def __new__(cls, clsname, bases, attrs, **kwargs):
        props = frozenset(kwargs.pop("props", set()))

        for prop in props:
            if not isinstance(prop, str): raise TypeError("Expected a set of strings")
            if cls.has_specials(prop): raise SyntaxError("Invalid identifier")
            attrs[prop] = None

        attrs.setdefault(f"_{cls.__name__}__props", props)
        attrs.setdefault(f"_{cls.__name__}__ifname", kwargs.pop("name", None))


        return super(InterfaceMeta, cls).__new__(
            cls, clsname, bases, attrs
        )

    def __init__(self, *args, **kwargs):
        super(InterfaceMeta, self).__init__(
            *args, **kwargs
        )

    @property
    def props(self):
        return self.__props

    @property
    def ifname(self):
        if self.__ifname: return self.__ifname
        return "{" + (', '.join(self.props)) + "}"

    @staticmethod
    def has_specials(s):
        import re
        return not bool(re.match(r'\w[a-zA-Z0-9_]*$', s))

    def special_fmt(cls, with_special, without_special):
        if InterfaceMeta.has_specials(cls.ifname): 
            return with_special.format(cls.ifname)
        return without_special.format(cls.ifname)

    def __repr__(cls):
        quoted_name = cls.special_fmt("{}", "'{}'")
        return f"<interface {quoted_name}>"

    def __and__(cls, other):
        return Interface(cls.props | other.props)

    def __or__(cls, other):
        return Interface(cls.props & other.props)

def Interface(properties): # properties = set or function
    kw = {}
    if callable(properties): 
        kw["name"] = properties.__name__
        properties = properties()
    kw["props"] = properties

    class c(metaclass=InterfaceMeta, **kw):
        @classmethod
        def __subclasshook__(cls, C):
            if cls is c:
                return all(any(prop in B.__dict__ for B in C.__mro__) for prop in cls.props)
            return NotImplemented
            
        def __init__(self, dict = {}, **kwargs):
            if dict != {}: self.__dict__.update(dict)
            if kwargs != {}: self.__dict__.update(kwargs)

            for prop in properties:
                if prop not in self.__dict__: raise NameError(f"Missing property '{prop}'")

        def __delattr__(self, name):
            if name not in self.__class__.props:
                return super().__delattr__(name)
            raise TypeError("Cannot delete interface properties")

        def __repr__(self):
            paren_name = self.__class__.special_fmt("({})", "{}")
            props = ', '.join(f"{k}={v}" for k, v in self.__dict__.items())
            return f"{paren_name}({props})"

    return c


@Interface
def Box(): return {"values"}

@Interface
def Boolean(): return {"truth"}

def SizedList(n): 
    @Interface
    def Sized(): return set(range(0, 10))
    return Sized

@Interface
def Thinker(): return {"think", "values"}

def smart_intersect(*interfaces):
    c = functools.reduce(lambda a, b: a | b, interfaces)
    c.resolve = lambda self: next((i for i in interfaces if isinstance(self, i)), Interface(set()))
    return c