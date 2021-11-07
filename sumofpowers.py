from math import comb
from fractions import Fraction

madd = lambda x, y: [v + y[i] for i, v in enumerate(x)]
smul = lambda x, s: [v * s for v in x]

class Matrix: #numpyyyyyye9ygiofghjdfuigj why
    def __init__(self, x):
        self.value = [[Fraction(i) for i in j] for j in x]
        self.rows = len(self.value)
        self.cols = len(self.value[0])

    def __repr__(self):
        return '\n'.join('[{}]'.format(', '.join(str(i) for i in j)) for j in self.value)
    
    def __getitem__(self, key):
        return self.value[key]

    def inv(self):
        m = self.value
        for i, row in enumerate(m):
            nr = [Fraction()] * len(row)
            nr[i] = Fraction(1)
            row.extend(nr)

        for i in range(self.cols):
           m[i] = smul(m[i], 1 / m[i][i])
           for j in range(i + 1, self.cols):
               m[j] = madd(smul(m[i], -m[j][i]), m[j])
        self.value = [col[self.cols:] for col in m]

def sum_of_powers(n, e=1):
    e += 1
    z = [[(-1) ** (i + j + 1) * comb(i, j) if i != j else 0 for j in range(0, e)] for i in range(1, e + 1)]
    coeffs = Matrix(z)
    coeffs.inv()
    coeffs = coeffs[-1]
    return sum(c * pow(n, i + 1) for i, c in enumerate(coeffs))

print(sum_of_powers(100000000000000000000000, 30))