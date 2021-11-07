"""
creation: March 31, 2021

Creates triplets (c, a, b) such that c! = a!b!
`python3 factdiv.py`
"""

from math import factorial

MAX_C = 720 # maximum value C will be, inclusive
factorials = []
triplets = []

for i in range(0, MAX_C + 1):
    fi = factorial(i)
    factorials.append(fi)

    for j in range(2, i - 1):
        fj = factorial(j)

        q, r = divmod(fi, fj)
        if r != 0: continue

        if q in factorials:
            triplets.append((i, j, factorials.index(q)))
        
print(triplets)