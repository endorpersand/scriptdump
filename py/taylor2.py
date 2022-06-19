"""
Feb 21, 2022
"""
from sympy import *
import math

x = Symbol('x')
y = Symbol('y')

expr = x * sin(y)

def all_coeffs(n):
    return [math.comb(n, i) for i in range(n + 1)]

def taylor(expr, a = 0, b = 0, h = x, k = y, n = 2):
    assert n >= 0

    approx = 0
    order = []

    for i in range(n + 1):
        if len(order) == 0:
            order = [expr]
        else:
            first_order = order[0]
            new_order = [diff(first_order, x)]
            new_order.extend(diff(e, y) for e in order)
            order = new_order
        
        for j, [c, e] in enumerate(zip(all_coeffs(i), order)):
            h_term = h ** (i - j) if (i - j) != 0 else 1
            k_term = k ** j if j != 0 else 1

            approx += c * h_term * k_term * e.subs(x, a).subs(y, b) / math.factorial(i)
        
    return approx