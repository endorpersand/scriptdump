"""
creation: unknown

Conversion to and from continued fractions

You can import these by module, or
`python3 -i fracsimp.py` to mess around with them in interactive mode
"""

from fractions import Fraction
from functools import reduce
from decimal import Decimal

def frac_simp(cont_frac):
    cont_frac = cont_frac[::-1]
    cont_frac[0] = Fraction(cont_frac[0])
    return reduce(lambda acc, cv: 1 / acc + cv, cont_frac)

def frac_expand(simp_frac):
    frac = []
    while True:
        (a, b) = divmod(simp_frac, 1)
        frac.append(a)
        if b == 0: break
        simp_frac = 1 / b
    return frac

