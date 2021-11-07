import re
from fractions import Fraction
from itertools import chain
from collections import Counter
from math import gcd as mgcd, prod
from functools import reduce

gcd = lambda args: reduce(lambda acc, cv: mgcd(acc, cv), args)
lsub = lambda l1, l2: [l1[i] - l2[i] for i in range(len(l1))]
lscale = lambda l, scalar: [elem * scalar for elem in l]

class Matrix:
    def __init__(self, l = [], r = None, c = None):
        self.l = l
        self.r = len(self.l) if r == None else r
        self.c = len(self.l[0]) if c == None else c
        if len(self.l) != self.r:
            self.l = self.l[:self.r]
            self.l = self.l + [[] for i in range(self.r - len(self.l))]
        self.l = [col[:self.c] for col in self.l]
        self.l = [col + [0] * (self.c - len(col)) for col in self.l]
        self.l = [[Fraction(elem) for elem in col] for col in self.l]

    def __repr__(self):
        matrix = [[int(elem) for elem in row] for row in self.l[:]]
        return repr(matrix)

    def solve(self):
        matrix = self.l
        if self.c != self.r + 1: raise ValueError('matrix is not n x (n + 1)')
        # gauss-jordan elimination
        for i in range(self.r):
            if matrix[i][i] == 0:
                try:
                    ni = next(j for (j, row) in [*enumerate(matrix)][i + 1:] if row[i] != 0)
                except StopIteration:
                    raise ValueError('system cannot be solved')
                matrix[i], matrix[ni] = matrix[ni], matrix[i]

            matrix[i] = lscale(matrix[i], 1 / matrix[i][i])
            for (j, row) in enumerate(matrix):
                if i != j: matrix[j] = lsub(row, lscale(matrix[i], matrix[j][i]))
        solved = [*zip(*matrix)][-1]
        if any([sol.denominator != 1 for sol in solved]):
            dprod = prod([sol.denominator for sol in solved])
            solved = [int(sol * dprod) for sol in solved]
            dgcd = gcd([sol for sol in solved])
            solved = [sol // dgcd for sol in solved]
        return [int(sol) for sol in solved]
    

def balance(eq):
    # tokenize eq
    eq = re.sub(r' ', '', eq)
    eq = re.split(r'(\+|->)', eq) #eq used later
    eq2 = [token for token in eq if token != '+']
    if not all([re.match(r'(?:(?:[A-Z][a-z]*\d*|\((?:[A-Z][a-z]*\d*)+\)\d+)+|->)$', token) for token in eq2]): raise SyntaxError('invalid unbalanced chemical equation') # verify chemical equation is valid
    eq2 = ['->' if token == '->' else re.findall(r'[A-Z][a-z]*\d*|\(|\)\d*', token) for token in eq2] # separate elements within compounds

    elemv = lambda token: re.sub(r'\d', '', token)
    subv = lambda token: 1 if (c := re.sub(r'[^\d]', '', token)) == '' else int(c)

    #count elements in each compound of each side
    count = [eq2[:eq2.index('->')], eq2[eq2.index('->') + 1:]] # lhs, rhs
    for (si, side) in enumerate(count):
        for (ci, compound) in enumerate(side):
            #replace parens w/ equivalent counterpart
            lparens = reversed([i for (i, v) in enumerate(compound) if v == '('])
            for lparen in lparens:
                rparen = next(i + lparen for (i, v) in enumerate(compound[lparen:]) if re.match(r'\)\d*', v))
                part = compound[lparen + 1 : rparen + 1]
                part[-1] = subv(part[-1]) # ')x' => int(x)
                part = [elemv(elem) + str(subv(elem) * part[-1]) for elem in part[:-1]]
                compound = compound[:lparen] + part + compound[rparen + 1:]
            #counting
            cmpdcounter = Counter()
            for elem in compound:
                cmpdcounter += Counter({elemv(elem): subv(elem)})
            side[ci] = cmpdcounter
        count[si] = side

    keys = [sorted(set(chain(*[compound.keys() for compound in side]))) for side in count]
    if keys[0] != keys[1]: raise NameError('element missing on side')
    keys = keys[0]
    mat = [[[compound[k] for k in keys] for compound in side] for side in count]
    mat[1] = [[-elem for elem in compound] for compound in mat[1]]
    mat = [*zip(*(mat[0] + mat[1]))]
    mat = [[*eq, 0] for eq in mat]
    mat = [lscale(row, Fraction(1, gcd(row))) for row in mat] # simplify each eq
    mat = [row for (i, row) in enumerate(mat) if i == mat.index(row)] # eliminate matching eqs

    # add a x1 = 1 equation and then slice matrix so that matrix is n x (n + 1)
    for i in range(l := len(mat[0]) - 1):
        x = [0] * l
        x[i] = 1
        x += [1]
        mat.append(x)
        mat = mat[len(mat) - len(mat[0]) + 1:]

    coeffs = Matrix(mat).solve()
    #print(coeffs)
    if any([coeff < 1 for coeff in coeffs]): raise(ValueError('a resulting coefficient returned zero or negative'))
    for (i, coeff) in enumerate(coeffs):
        if coeff != 1: eq[2 * i] = str(coeff) + eq[2 * i]
    return ' '.join(eq)
    #print(mat)
    #print(count, keys)

print(balance('K4Fe(SCN)6 + K2Cr2O7 + H2SO4 -> Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3'))

if __name__ == '__main__':
    print(balance(input('Input unbalanced equation. \nex. ' + '\033[0;33m' + 'Cu + HNO3 -> Cu(NO3)2 + NO + H2O\n' + '\033[0m' + '>>> ')))
    while True:
        print(balance(input('>>> ')))