"""
creation: Nov 28, 2021

Prime factorization & is_prime checking using Miller-Rabin
https://en.wikipedia.org/wiki/Miller–Rabin_primality_test
"""
import math
from enum import Enum, auto

class MRResult(Enum):
    CERTAIN = auto()
    UNCERTAIN = auto()

# def is_prime_slow(n: int) -> bool:
#     if n < 2: return False
#     if n % 2 == 0: return False

#     isq = math.isqrt(n)
#     return all(n % i != 0 for i in range(3, isq + 1, 2))


def decompose_n(n: int) -> tuple[int, int]:
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    return (r, d)

def mr_test(n: "int | tuple[int, int]", a: int) -> bool:  # type: ignore
    if isinstance(n, tuple): 
        r, d = n
        n: int = 2 ** r * d + 1
    else: 
        r, d = decompose_n(n)
    
    x = pow(a, d, n)
    if x in (1, n - 1): return True
    for _ in range(r - 1):
        x = pow(x, 2, n)
        if x == n - 1: return True
    return False

def is_prime(n: int) -> tuple[MRResult, bool]:
    witnesses = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    maximum = 3317044064679887385961981

    if n in witnesses: return MRResult.CERTAIN, True
    if n < 2: return MRResult.CERTAIN, False
    if n % 2 == 0: return MRResult.CERTAIN, False
    
    r, d = decompose_n(n)

    result = all(mr_test((r,d), a) for a in witnesses)
    if result:
        return (MRResult.CERTAIN if n < maximum else MRResult.UNCERTAIN,
               result)

    return MRResult.CERTAIN, result


### FACTORIZATION

# def factor_slow(n: int) -> tuple[int, ...]:
#     if 0 <= n < 2: return (n, )

#     factors = []

#     if n < 0:
#         factors.append(-1)
#         n *= -1

#     while n % 2 == 0:
#         factors.append(2)
#         n //= 2

#     isq = math.isqrt(n)
#     for i in range(3, isq + 1, 2):
#         if n < i: break
#         while n % i == 0:
#             factors.append(i)
#             n //= i
    
#     if n != 1: factors.append(n)
#     return tuple(factors)

def factor(n: int, stop=1000000) -> tuple[tuple[int, ...], "tuple[MRResult, bool] | None"]:
    if 0 <= n < 2: return (n, ), None

    factors = []

    if n < 0:
        factors.append(-1)
        n *= -1

    while n % 2 == 0:
        factors.append(2)
        n //= 2

    isq = math.isqrt(n)

    for i in range(3, min(isq + 1, stop), 2):
        if n == 1: break
        while n % i == 0:
            factors.append(i)
            n //= i
    
    if n != 1: 
        pr = is_prime(n)
        factors.append(n)
        return tuple(factors), pr
    return tuple(factors), None
