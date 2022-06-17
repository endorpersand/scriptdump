"""
Prime factorization & primality checking using Lenstra elliptic-curve factorization
https://en.wikipedia.org/wiki/Lenstra_elliptic-curve_factorization
"""

import dataclasses
import itertools
import math
import random

class SlopeFailure(Exception): pass
class HitInfinity(SlopeFailure): pass
@dataclasses.dataclass
class HitFactor(SlopeFailure):
    factor: int

Point = tuple[int, int]
@dataclasses.dataclass
class Curve:
    A: int
    B: int
    n: int

    def __iter__(self):
        return iter((self.A, self.B, self.n))

    @classmethod
    def random(cls, n: int) -> "tuple[Curve, Point]":
        def rr(): 
            while True: yield random.randrange(n)
        gen = filter(lambda r: math.gcd(r, n) == 1, rr())
        x0 = next(gen)
        y0 = next(gen)
        A  = next(gen)

        B = (pow(y0, 2, n) - pow(x0, 3, n) - A * x0) % n

        return (cls(A, B, n), (x0, y0))
    
    def pow(self, a: int, b: int):
        return pow(a, b, self.n)

    def __contains__(self, pt: Point) -> bool:
        x, y = pt
        A, B, n = self

        return self.pow(y, 2) == (self.pow(x, 3) + A * x + B) % n
    
    def __str__(self):
        A, B, n = self
        return f"y^2 = x^3 + {A}x + {B} (mod {n})"

    def tangent(self, pt: Point):
        x, y = pt
        A, _, n = self

        # we're calculating u / v
        v = (2 * y) % n

        if v == 0: raise HitInfinity
        elif (gcd := math.gcd(v, n)) != 1: raise HitFactor(gcd)

        u = 3 * self.pow(x, 2) + A
        return (u * self.pow(v, -1)) % n

    def secant(self, p: Point, q: Point):
        px, py = p
        qx, qy = q
        n = self.n

        v = (qx - px) % n

        if v == 0: raise HitInfinity
        elif (gcd := math.gcd(v, n)) != 1: raise HitFactor(gcd)

        u = qy - py
        return (u * self.pow(v, -1)) % n

    def raw_add(self, s: int, p: Point, q: Point):
        px, py = p
        qx, _  = q
        n = self.n

        rx = (self.pow(s, 2) - px - qx) % n
        ry = (s * (px - rx) - py) % n

        return (rx, ry)

    def add(self, p: Point, q: Point):
        return self.raw_add(self.secant(p, q), p, q)

    def double(self, p: Point):
        return self.raw_add(self.tangent(p), p, p)
    
    def mul(self, p: Point, n: int):
        r = p
        for b in f"{n:b}"[1:]:
            r = self.double(r)
            if b == "1":
                r = self.add(r, p)
            
        return r

def repeat_pop(n: int, ftr: int, flist: list):
    mult = 0
    while n % ftr == 0:
        mult += 1
        n //= ftr
    
    flist.extend(itertools.repeat(ftr, times=mult))
    return n

def factor(n: int, B=500):
    if 0 <= n < 2: return (n, ), None

    factors: list[int] = []

    if n < 0:
        factors.append(-1)
        n *= -1

    n = repeat_pop(n, 2, factors)
    
    while n != 1:
        c, p = Curve.random(n)
        print(c)
        for i in range(2, B):
            try:
                p = c.mul(p, i)
            except HitFactor as e:
                n = repeat_pop(n, e.factor, factors)
                break
            except HitInfinity:
                factors.append(n)
                n = 1
                break
    
    return tuple(factors)
