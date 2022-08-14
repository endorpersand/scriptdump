from fractions import Fraction
import itertools
import math
import numbers
import operator


def estr(s):
    if isinstance(s, Expr): return f"({s})"
    return f"{s}"

def is_integral(n):
    return isinstance(n, numbers.Rational) and n.denominator == 1

def rational_div(a, b):
    if b == 0: return None
    return Fraction(a, b)

def rational_pow(a, b):
    if a == 0 and b == 0: return None
    if a == 0: return 0
    if a == 1: return 1
    if b == 0: return 1

    if isinstance(a, numbers.Rational) and is_integral(b): 
        if a < 100 and b < 100:
            return pow(a, b)
    return None

def rational_log(base, x):
    try:
        l = round(math.log(x, base))
        if base ** l == x: return l
    except (ValueError, ZeroDivisionError):
        return None

def rational_factorial(a):
    if a < 0 or a > 100: return None
    return math.factorial(a)

BINOPS = {
    "+": operator.add, 
    "-": operator.sub, 
    "*": operator.mul, 
    "/": rational_div,
    "^": rational_pow,
    "log": rational_log
}
B_INVERSES = {
    "left": {
        # a + X = c, X = c - a
        "+":   lambda a, c: c - a,
        # a - X = c, X = a - c
        "-":   lambda a, c: a - c, 
        # a * X = c, X = c / a
        "*":   lambda a, c: rational_div(c, a),
        # a / X = c, X = a / c
        "/":   lambda a, c: rational_div(a, c),
        # a ^ X = c, X = log_a(c)
        "^":   lambda a, c: rational_log(a, c),
        # log_a(X) = c, X = a^c
        "log": lambda a, c: rational_pow(a, c)
    },
    "right": {
        # X + a = c, X = c - a
        "+":   lambda a, c: c - a,
        # X - a = c, X = c + a
        "-":   lambda a, c: c + a, 
        # X * a = c, X = c / a
        "*":   lambda a, c: rational_div(c, a),
        # X / a = c, X = c * a
        "/":   lambda a, c: c * a,
        # X ^ a = c, X = c ^ (1/a)
        "^":   lambda a, c: rational_pow(c, rational_div(1, a)),
        # log_X(a) = c, X = a ^ (1/c)
        "log": lambda a, c: rational_pow(a, rational_div(1, c))
    },
}

PRINT = {
    "log": lambda a, b: f"log_{a}({b})",
}

class Expr:
    op: str
    args: list

    def __new__(cls, op, args):
        o = object.__new__(cls)
        o.op = op
        o.args = args
        return o
    

    def __str__(self):
        if self.op in PRINT:
            return PRINT[self.op](*self.args)

        if len(self.args) == 2:
            a, b = self.args
            return f"{estr(a)} {self.op} {estr(b)}"

        return "{}({})".format(self.op, ','.join(estr(a) for a in self.args))
    
    def __add__(self, other): return Expr("+", [self, other])
    def __sub__(self, other): return Expr("-", [self, other])
    def __mul__(self, other): return Expr("*", [self, other])
    def __div__(self, other): return Expr("/", [self, other])
    def __xor__(self, other): return Expr("^", [self, other])
    def __pow__(self, other): return Expr("^", [self, other])
    def __radd__(self, other): return Expr("+", [other, self])
    def __rsub__(self, other): return Expr("-", [other, self])
    def __rmul__(self, other): return Expr("*", [other, self])
    def __rdiv__(self, other): return Expr("/", [other, self])
    def __rxor__(self, other): return Expr("^", [other, self])
    def __rpow__(self, other): return Expr("^", [other, self])
    
class SExpr(Expr):
    def __new__(cls, op, args):
        # simplify
        if op == "^":
            a, b = args
            
            if isinstance(b, numbers.Rational):
                if isinstance(a, SExpr):
                    if a.op in ("*", "/"):
                        return cls(a.op, [cls("^", [arg, b]) for arg in a.args])
                    elif a.op in "^":
                        return cls(a.op, [a.args[0], a.args[1] * b])
        
        if all(isinstance(a, numbers.Rational) for a in args) and op in BINOPS:
            result = BINOPS[op](*args)
            if result is not None:
                return result
        
        return super().__new__(cls, op, args)
    
    @classmethod
    def simplify(cls, e):
        if isinstance(e, Expr) and not isinstance(e, cls):
            return cls(e.op, [cls.simplify(a) for a in e.args])
        return e
    
DIGITS = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
}
N_DIGITS = 4 # this has to be 4
RESULT = 24

def inverse(op, result, other, other_is_right):
    inv = B_INVERSES["right" if other_is_right else "left"][op](other, result)
    
    oper = BINOPS[op]
    if inv is not None:
        valid_inv = (
            (other_is_right and oper(inv, other) == result) or
            (not other_is_right and oper(other, inv) == result)
        )

        if valid_inv: return inv

INVERSE_MAP = {
    "left": {
        d: {
            k: b 
            for b in BINOPS
            if (k := inverse(b, RESULT, d, False)) is not None
        } 
        for d in DIGITS
    },
    "right": {
        d: {
            k: b 
            for b in BINOPS
            if (k := inverse(b, RESULT, d, True)) is not None
        } 
        for d in DIGITS
    }
}


def construct(digits: "tuple[int]", ops: "tuple[str]", order: "tuple[int]") -> Expr:
    refs = [*range(len(digits))]
    vals = [*digits]

    for i in order:
        ai, bi = refs[i], refs[i + 1]

        vals[ai:bi + 1] = [Expr(
            ops[i],
            [vals[ai], vals[bi]]
        )]

        merged = min(ai, bi)
        # two values got merged into 1, so value positions should be decremented
        for j, r in enumerate(refs):
            if r > merged: refs[j] -= 1
    
    return vals[0]

def exprs_of(digits):
    [lother, *rest] = digits
    rest_vals = INVERSE_MAP["left"][lother]

    n_ops = N_DIGITS - 2
    for ops in itertools.product(BINOPS, repeat=n_ops):
        for order in itertools.permutations(range(n_ops), n_ops):
            tree = construct(rest, ops, order)
            
            v = SExpr.simplify(tree)
            if v in rest_vals:
                yield Expr(rest_vals[v], [lother, tree])
    
    [*rest, rother] = digits
    rest_vals = INVERSE_MAP["right"][rother]

    n_ops = N_DIGITS - 2
    for ops in itertools.product(BINOPS, repeat=n_ops):
        for order in itertools.permutations(range(n_ops), n_ops):
            tree = construct(rest, ops, order)
            
            v = SExpr.simplify(tree)
            if v in rest_vals:
                yield Expr(rest_vals[v], [tree, rother])
    
    [d1, d2, d3, d4] = digits
    for [o1, o2, o3] in itertools.product(BINOPS, repeat=3):
        yield Expr(o2, [Expr(o1, [d1, d2]), Expr(o3, [d3, d4])])

def test_digits(digits):
    for tree in exprs_of(digits):
        if SExpr.simplify(tree) == RESULT:
            return tree

with open("24.txt", "w") as f:
    for digits in itertools.product(DIGITS, repeat=N_DIGITS):
        tree = test_digits(digits)

        n = "".join(DIGITS[d] for d in digits)
        
        if tree is not None:
            f.write(f"{n}: {tree}")
        else:
            f.write(f"{n}: :(")
        f.write("\n")
        f.flush()