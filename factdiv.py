from math import factorial

factorials = []
triplets = []

for i in range(0, 721):
    fi = factorial(i)
    factorials.append(fi)

    for j in range(2, i - 1):
        fj = factorial(j)

        q, r = divmod(fi, fj)
        if r != 0: continue

        if q in factorials:
            triplets.append((i, j, factorials.index(q)))
        
print(triplets)