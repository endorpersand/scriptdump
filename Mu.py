import inspect
import re
class _MuMod:
    def __init__(self, f):
        self.f = f

    def __call__(self, code: str):
        return self.f(code)

class Mu:
    '''
    Function morpher, via docstrings.
    '''
    Mod = _MuMod

    def __new__(cls, *mods):
        if all(isinstance(mod, cls.Mod) for mod in mods): return cls._morph(*mods)
        if len(mods) == 1 and not isinstance(mods[0], cls.Mod): return cls._morph(cls.default)(mods[0])
        raise TypeError("Attempted to morph with a non-mod")
    
    @classmethod
    def _morph(cls, *mods):
        def d(f):
            sig = inspect.signature(f)
            code = f.__doc__
            for mf in mods:
                code = mf(code)

            full = f"def {f.__name__}{sig}:" + code
            exec(full)
            return locals()[f.__name__]
        return d

    @Mod
    def identity(code: str):
        return code


@Mu
def a(b):
    """
    return False
    """

print(a(1))