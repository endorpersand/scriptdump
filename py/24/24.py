import fractions
import operator
import itertools

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
OPERATIONS = {
    "+": operator.add, 
    "-": operator.sub, 
    "*": operator.mul, 
    "/": fractions.Fraction
}
N_DIGITS = 4
RESULT = 24

def construct(digits: "tuple[int]", ops: "tuple[str]", order: "tuple[int]"):
    refs = [*range(len(digits))]
    vals = [*digits]

    for i in order:
        ai, bi = refs[i], refs[i + 1]

        vals[ai:bi + 1] = [{
            "op": ops[i],
            "args": [vals[ai], vals[bi]]
        }]

        merged = min(ai, bi)
        # two values got merged into 1, so value positions should be decremented
        for j, r in enumerate(refs):
            if r > merged: refs[j] -= 1
    
    return vals[0]

def eval_tree(tree):
    if isinstance(tree, dict): 
        a, b = tree['args']
        
        if isinstance(a, dict): a = eval_tree(a)
        if isinstance(b, dict): b = eval_tree(b)

        if a is not None and b is not None:
            try:
                return OPERATIONS[tree["op"]](a, b)
            except ZeroDivisionError:
                pass
        return None
    return tree

def tree_str(tree, paren=False):
    if isinstance(tree, dict): 
        a, b = tree['args']
        
        s = f"{tree_str(a, True)} {tree['op']} {tree_str(b, True)}"
        
        if paren: return f"({s})"
        return s
    
    return tree

def exprs_of(digits):
    n_ops = N_DIGITS - 1
    for ops in itertools.product(OPERATIONS, repeat=n_ops):
        for order in itertools.permutations(range(n_ops), n_ops):
            yield construct(digits, ops, order)

def test_digits(digits):
    for tree in exprs_of(digits):
        if eval_tree(tree) == RESULT:
            return tree

with open("24.txt", "w") as f:
    for digits in itertools.product(DIGITS, repeat=N_DIGITS):
        tree = test_digits(digits)

        n = "".join(DIGITS[d] for d in digits)
        
        if tree is not None:
            f.write(f"{n}: {tree_str(tree)}")
        else:
            f.write(f"{n}: :(")
        f.write("\n")