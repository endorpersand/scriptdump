"""
creation: November 6, 2021

Requires Python 3.10
This allows you to do simple operations with multivectors!

There's one function: Multivector(n)
- Takes in a dimension (e.g. 2, 3) and gives you n basis vectors in a tuple
- example: `e1, e2, e3 = Multivector(3)`
- You can do algebra with those basis vectors!

Supported operations:
- Addition, subtraction
- Geometric product (a * b)
- Exterior product (a ^ b)
- Scalar division

If you'd like to experiment, `python3 -i Multivector.py` gives you 3 basis vectors (e1, e2, e3)
You can also just import as a module (`from Multivector import *`)
or... use a good GA library like clifford.
"""

__all__ = ("Multivector",)
class _Blade:
        def __init__(self, ind: int, scale: int | float = 1):
            self.basis = ind
            self.scale = scale
        
        def __repr__(self):
            s, b = self.scale, self.basis
            buf = []
            if s == 0: return str(0)
            if b == 0: return str(s)
            if s == -1: buf.append("-")
            elif s != 1: buf.append(str(s))

            for i in range(b.bit_length()):
                if (b >> i) & 0b1:
                    buf.append(f"e{i + 1}")
            return "".join(buf)
        
        def __eq__(self, o):
            return self.__class__ == o.__class__ and self.basis == o.basis and self.scale == o.scale

        def __neg__(self):
            return self.__class__(self.basis, -self.scale)

        # geometric product
        def __mul__(self, ro: "int | float | _Blade"):
            if isinstance(ro, int | float): return self.__class__(self.basis, self.scale * ro)
            
            if isinstance(ro, self.__class__):
                b1, b2 = self.basis, ro.basis
                s1, s2 = self.scale, ro.scale
                
                bf = 0
                sf = s1 * s2
                for i in range(max(b1.bit_length(), b2.bit_length())):
                    b1_axis, b1_rest = (b1 >> i) & 0b1, b1 >> (i + 1)
                    b2_axis = (b2 >> i) & 0b1

                    bf |= (b1_axis ^ b2_axis) << i
                    if b2_axis & (b1_rest.bit_count() & 0b1): sf *= -1
                return self.__class__(bf, sf)
            
            return NotImplemented
        
        def __rmul__(self, lo: "int | float"):
            if isinstance(lo, int | float): return self.__class__(self.basis, self.scale * lo)
            return NotImplemented

def Multivector(n: int):
    class _MV:
        def __init__(self, it = ()):
            size = 1 << n
            tpl = tuple(it)
            self._vals = tpl[:size] + (0,) * (size - len(tpl))
        
        @classmethod
        def _from_blade(cls, blade: int | float | _Blade) -> "_MV":
            if isinstance(blade, _Blade): return cls((0,) * blade.basis + (blade.scale,))
            if isinstance(blade, int | float): return cls((blade,))
            if isinstance(blade, cls): return blade
            raise TypeError(f"Cannot convert type {blade.__class__.__name__} to {cls.__name__}")

        def __repr__(self) -> str:
            if not any(self._vals): return str(0)
            s = " + ".join(str(_Blade(i, s)) for i, s in enumerate(self._vals) if s != 0)
            return s.replace("+ -", "- ")

        def __eq__(self, o):
            return self.__class__ == o.__class__ and self._vals == o._vals

        def __neg__(self):
            return self.__class__(-a for a in self._vals)

        def __add__(self, ro):
            return self.__class__(a + b for a, b in zip(self._vals, self._from_blade(ro)._vals))
            
        def __radd__(self, lo):
            return self.__add__(lo)
        
        def __sub__(self, ro):
            return self.__add__(-ro)
            
        def __rsub__(self, lo):
            return (-self).__add__(lo)
        
        # geometric product
        def __mul__(self, ro):
            out = [0] * len(self._vals)
            for i, s1 in (t for t in enumerate(self._vals) if t[1] != 0):
                for j, s2 in (t for t in enumerate(self._from_blade(ro)._vals) if t[1] != 0):
                    bf = _Blade(i, s1) * _Blade(j, s2)
                    out[bf.basis] += bf.scale
            
            return self.__class__(out)

        def __rmul__(self, lo):
            return self._from_blade(lo).__mul__(self)
        
        def __getitem__(self, i):
            if not isinstance(i, int): return NotImplemented
            return self.__class__(v if b.bit_count() == i else 0 for b, v in enumerate(self._vals))

        # dot product
        def __matmul__(self, ro):
            out = 0
            for r in range(len(self._vals).bit_length()):
                for s in range(len(self._from_blade(ro)._vals).bit_length()):
                    out += (self[r] * ro[s])[s - r]
            return out

        # exterior product
        def __xor__(self, ro):
            ro = self._from_blade(ro)
            out = 0
            for r in range(len(self._vals).bit_length()):
                for s in range(len(ro._vals).bit_length()):
                    out += (self[r] * ro[s])[r + s]
            return out

        def __rxor__(self, lo):
            return self._from_blade(lo).__xor__(self)

        def __truediv__(self, ro):
            if isinstance(ro, _MV):
                if not any(ro[1:]): return self / ro._vals[0]
            
            return self.__class__(v / ro for v in self._vals)
        def __floordiv__(self, ro):
            if isinstance(ro, _MV):
                if not any(ro[1:]): return self // ro._vals[0]
            
            return self.__class__(v // ro for v in self._vals)

    _MV.__name__ = f"_MV{n}_{hex(id(_MV))}"
    return tuple(
        _MV._from_blade(_Blade(1 << i)) for i in range(n)
    )

if __name__ == "__main__":
    e1, e2, e3 = Multivector(3)