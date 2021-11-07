"""
creation: July 22-26, 2021

System for calculating the optimal nuclear decay path for reactors in Omnifactory.
Have fun looking at it!
"""

from dataclasses import dataclass
from fractions import Fraction
from numbers import Rational
from itertools import chain, product

inf = float('inf')
def div(a, b):
    return Fraction(1,1) * a / b

@dataclass(frozen=True)
class Item:
    name: str
    qty: Rational = 1

    def __str__(self):
        qty = f"{float(self.qty):01.5f}"
        return f"{qty}x {self.name}"

@dataclass
class Recipe:
    i: list[Item]
    o: list[Item]

    def __matmul__(self, other):
        if self.i is None: return self.__class__(other, self.o)
        if self.o is None: return self.__class__(self.i, other)
        return self
    
    __rshift__ = __matmul__

    def __str__(self):
        return f"{self.pretty_list(self.i)} -> {self.pretty_list(self.o)}"

    @staticmethod
    def pretty_list(lst: "list[Item]", sep=", ", outer=True):
        inner = sep.join(str(e) for e in lst if not str(e).startswith("0.0000"))
        return f"[{inner}]" if outer else inner

    @staticmethod
    def pprint(lst: "list[Item]", sep="\n", outer=False):
        print(Recipe.pretty_list(lst, sep, outer))
    

    @staticmethod
    def item_qty(inputs: "list[Item]", item: str):
        return sum(it.qty for it in inputs if it.name == item)

    @staticmethod
    def scale(inputs: "list[Item]", n: Rational):
        return [Item(it.name, it.qty * n) for it in inputs]

    @staticmethod
    def add(*inputses: "tuple[list[Item]]"):
        its = [*chain.from_iterable(inputses)]
        return [*filter(lambda it: it.qty != 0, (Item(name, Recipe.item_qty(its, name)) for name in set(it.name for it in its)))]

    def has_all_ingredients(self, inputs: "list[Item]") -> bool:
        iset, rset = set(it.name for it in inputs), set(it.name for it in self.i)
        return rset <= iset

    def calculate(self, inputs: "list[Item]") -> "list[Item]":
        inputs = inputs.copy()

        if not self.has_all_ingredients(inputs): return inputs

        n_outputs = min(div(self.item_qty(inputs, it.name), it.qty) for it in self.i)
        return self.add(inputs, self.scale(self.i, -1 * n_outputs), self.scale(self.o, n_outputs))



Recipe = Recipe(None, None)

# a while ago, 2021

main_recipes = [
    Recipe @ [Item("TBU")] >> [
        Item("U233",  div(16, 9)),
        Item("Np236", div(8, 9)),
        Item("Np237", div(32, 9)),
    ]
]
low_recipes = [
    Recipe @ [Item("U233", 1),  Item("U238", 8)] >>  [Item("LEU-233")],
    Recipe @ [Item("Np236", 1), Item("Np237", 8)] >> [Item("LEN-236")],
    Recipe @ [Item("Pu239", 1), Item("Pu242", 8)] >> [Item("LEP-239")],
    Recipe @ [Item("Am242", 1), Item("Am243", 8)] >> [Item("LEA-242")],
    Recipe @ [Item("LEU-233")] >> [
        Item("Pu239", div(4, 9)),
        Item("Pu241", div(4, 9)),
        Item("Pu242", div(32, 9)),
        Item("Am243", div(24, 9))
    ],
    Recipe @ [Item("LEN-236")] >> [
        Item("Np237", div(4, 9)),
        Item("Pu242", div(32, 9)),
        Item("Am242", div(8, 9)),
        Item("Am243", div(20, 9))
    ],
    Recipe @ [Item("LEP-239")] >> [
        Item("Pu239", div(8, 9)),
        Item("Pu242", div(24, 9)),
        Item("Cm243", div(4, 9)),
        Item("Cm246", div(28, 9))
    ],
    Recipe @ [Item("LEA-242")] >> [
        Item("Cm243", div(8, 9)),
        Item("Cm245", div(8, 9)),
        Item("Cm246", div(40, 9)),
        Item("Cm247", div(8, 9))
    ],
]
high_recipes = [
    Recipe @ [Item("U233", 4),  Item("U238", 5)]  >> [Item("HEU-233")],
    Recipe @ [Item("Np236", 4), Item("Np237", 5)] >> [Item("HEN-236")],
    Recipe @ [Item("Pu239", 4), Item("Pu242", 5)] >> [Item("HEP-239")],
    Recipe @ [Item("Am242", 4), Item("Am243", 5)] >> [Item("HEA-242")],
    Recipe @ [Item("HEU-233")] >> [
        Item("Np236", div(32, 9)),
        Item("Np237", div(8, 9)),
        Item("Pu242", div(16, 9)),
        Item("Am243", div(8, 9))
    ],
    Recipe @ [Item("HEN-236")] >> [
        Item("U238",  div(16, 9)),
        Item("Pu238", div(8, 9)),
        Item("Pu239", div(8, 9)),
        Item("Pu242", div(32, 9))
    ],
    Recipe @ [Item("HEP-239")] >> [
        Item("Am241", div(8, 9)),
        Item("Am242", div(24, 9)),
        Item("Cm245", div(8, 9)),
        Item("Cm246", div(24, 9))
    ],
    Recipe @ [Item("HEA-242")] >> [
        Item("Cm245", div(16, 9)),
        Item("Cm246", div(32, 9)),
        Item("Cm247", div(8, 9)),
        Item("Bk247", div(8, 9))
    ],
]

sunnarium_recipes = [
    Recipe @ [Item("Pu"), Item("Cm")] >> [Item("Sun")],
    Recipe @ [Item("Sun"), Item("Np", 4), Item("Am", 4)] >> [Item("ESun", 4)],

    Recipe @ [Item("Pu238")] >> [Item("Pu", 2)],
    Recipe @ [Item("Pu239")] >> [Item("Pu", 2)],
    Recipe @ [Item("Pu241")] >> [Item("Pu", 2)],
    Recipe @ [Item("Pu242")] >> [Item("Pu", 2)],
    Recipe @ [Item("Pu244")] >> [Item("Pu", 2)],

    Recipe @ [Item("Cm243")] >> [Item("Cm", 4)],
    Recipe @ [Item("Cm245")] >> [Item("Cm", 4)],
    Recipe @ [Item("Cm246")] >> [Item("Cm", 4)],
    Recipe @ [Item("Cm247")] >> [Item("Cm", 4)],

    Recipe @ [Item("Np236")] >> [Item("Np", 2)],
    Recipe @ [Item("Np237")] >> [Item("Np", 2)],

    Recipe @ [Item("Am241")] >> [Item("Am", 4)],
    Recipe @ [Item("Am242")] >> [Item("Am", 4)],
    Recipe @ [Item("Am243")] >> [Item("Am", 4)],

    Recipe @ [Item("Bk247")] >> [Item("Bk", 8)],
    Recipe @ [Item("Bk248")] >> [Item("Bk", 8)],

    Recipe @ [Item("Cf249")] >> [Item("Cf", 8)],
    Recipe @ [Item("Cf250")] >> [Item("Cf", 8)],
    Recipe @ [Item("Cf251")] >> [Item("Cf", 8)],
    Recipe @ [Item("Cf252")] >> [Item("Cf", 8)],
]

inventory = [
    Item("TBU", 1),
    # Item("U238", inf)
]

def run_recipes(recipes, inv, MAX_ITERS=100, p=True):
    iminv = inv.copy()
    iterations = 0
    while any(r.has_all_ingredients(iminv) for r in recipes) and iterations <= MAX_ITERS:
        for r in recipes:
            if r.has_all_ingredients(iminv):
                #print(f"Crafted: {r}")
                iminv = r.calculate(iminv)
                iterations += 1

    if p: Recipe.pprint(iminv)
    return iminv

# print("LE* Recipes")
# lei = run_recipes([*main_recipes, *low_recipes], inventory)
# print()
# print("HE* Recipes")
# hei = run_recipes([*main_recipes, *high_recipes], inventory)
# print()
# print("HE* Recipes + LEA-242")
# hel242i = run_recipes([*main_recipes, *high_recipes[:3], *high_recipes[4:-1], low_recipes[3], low_recipes[-1]], inventory)
# print()

# print("LE* Recipes")
# run_recipes(sunnarium_recipes, lei)
# print()
# print("HE* Recipes")
# run_recipes(sunnarium_recipes, hei)
# print()
# print("HE* Recipes + LEA-242")
# run_recipes(sunnarium_recipes, hel242i)

# Jul 25, 2021

mrec = [
    Recipe @ [Item("TBU")] >> [
        Item("U233",  div(16, 9)),
        Item("Np236", div(8, 9)),
        Item("Np237", div(32, 9)),
    ],
    Recipe @ [Item("LEU-233")] >> [
        Item("Pu239", div(4, 9)),
        Item("Pu241", div(4, 9)),
        Item("Pu242", div(32, 9)),
        Item("Am243", div(24, 9))
    ],
    Recipe @ [Item("LEN-236")] >> [
        Item("Np237", div(4, 9)),
        Item("Pu242", div(32, 9)),
        Item("Am242", div(8, 9)),
        Item("Am243", div(20, 9))
    ],
    Recipe @ [Item("LEP-239")] >> [
        Item("Pu239", div(8, 9)),
        Item("Pu242", div(24, 9)),
        Item("Cm243", div(4, 9)),
        Item("Cm246", div(28, 9))
    ],
    Recipe @ [Item("LEA-242")] >> [
        Item("Cm243", div(8, 9)),
        Item("Cm245", div(8, 9)),
        Item("Cm246", div(40, 9)),
        Item("Cm247", div(8, 9))
    ],
    Recipe @ [Item("HEU-233")] >> [
        Item("Np236", div(32, 9)),
        Item("Np237", div(8, 9)),
        Item("Pu242", div(16, 9)),
        Item("Am243", div(8, 9))
    ],
    Recipe @ [Item("HEN-236")] >> [
        Item("U238",  div(16, 9)),
        Item("Pu238", div(8, 9)),
        Item("Pu239", div(8, 9)),
        Item("Pu242", div(32, 9))
    ],
    Recipe @ [Item("HEP-239")] >> [
        Item("Am241", div(8, 9)),
        Item("Am242", div(24, 9)),
        Item("Cm245", div(8, 9)),
        Item("Cm246", div(24, 9))
    ],
    Recipe @ [Item("HEA-242")] >> [
        Item("Cm245", div(16, 9)),
        Item("Cm246", div(32, 9)),
        Item("Cm247", div(8, 9)),
        Item("Bk247", div(8, 9))
    ],
]
lrec = [
    Recipe @ [Item("U233", 1),  Item("U238", 8)] >>  [Item("LEU-233")],
    Recipe @ [Item("Np236", 1), Item("Np237", 8)] >> [Item("LEN-236")],
    Recipe @ [Item("Pu239", 1), Item("Pu242", 8)] >> [Item("LEP-239")],
    Recipe @ [Item("Am242", 1), Item("Am243", 8)] >> [Item("LEA-242")],
]
hrec = [
    Recipe @ [Item("U233", 4),  Item("U238", 5)]  >> [Item("HEU-233")],
    Recipe @ [Item("Np236", 4), Item("Np237", 5)] >> [Item("HEN-236")],
    Recipe @ [Item("Pu239", 4), Item("Pu242", 5)] >> [Item("HEP-239")],
    Recipe @ [Item("Am242", 4), Item("Am243", 5)] >> [Item("HEA-242")]
]

# out = []
# for i in range(16):
#     chosen_rec = [lrec[j] if int(sel) == 0 else hrec[j] for j, sel in enumerate(f"{i:04b}")]
#     print(f"Set {i:04b}")
#     out.append(run_recipes([*mrec, *chosen_rec], inventory))
#     print()

# for i, e in enumerate(out):
#     print(f"Set {i:04b}")
#     run_recipes(sunnarium_recipes, e)
#     print()

# Jul 25, 2021, 15:29

mrec = [
    Recipe @ [Item("TBU")] >> [
        Item("U233",  div(16, 9)),
        Item("Np236", div(8, 9)),
        Item("Np237", div(32, 9)),
    ],

    Recipe @ [Item("LEU-233")] >> [
        Item("Pu239", div(4, 9)),
        Item("Pu241", div(4, 9)),
        Item("Pu242", div(32, 9)),
        Item("Am243", div(24, 9))
    ],
    Recipe @ [Item("HEU-233")] >> [
        Item("Np236", div(32, 9)),
        Item("Np237", div(8, 9)),
        Item("Pu242", div(16, 9)),
        Item("Am243", div(8, 9))
    ],

    Recipe @ [Item("LEN-236")] >> [
        Item("Np237", div(4, 9)),
        Item("Pu242", div(32, 9)),
        Item("Am242", div(8, 9)),
        Item("Am243", div(20, 9))
    ],
    Recipe @ [Item("HEN-236")] >> [
        Item("U238",  div(16, 9)),
        Item("Pu238", div(8, 9)),
        Item("Pu239", div(8, 9)),
        Item("Pu242", div(32, 9))
    ],

    Recipe @ [Item("LEP-239")] >> [
        Item("Pu239", div(8, 9)),
        Item("Pu242", div(24, 9)),
        Item("Cm243", div(4, 9)),
        Item("Cm246", div(28, 9))
    ],
    Recipe @ [Item("LEP-241")] >> [
        Item("Pu242", div(4, 9)),
        Item("Am242", div(4, 9)),
        Item("Am243", div(8, 9)),
        Item("Cm246", div(48, 9))
    ],
    Recipe @ [Item("HEP-239")] >> [
        Item("Am241", div(8, 9)),
        Item("Am242", div(24, 9)),
        Item("Cm245", div(8, 9)),
        Item("Cm246", div(24, 9))
    ],
    Recipe @ [Item("HEP-241")] >> [
        Item("Am241", div(8, 9)),
        Item("Cm245", div(8, 9)),
        Item("Cm246", div(24, 9)),
        Item("Cm247", div(24, 9))
    ],

    Recipe @ [Item("LEA-242")] >> [
        Item("Cm243", div(8, 9)),
        Item("Cm245", div(8, 9)),
        Item("Cm246", div(40, 9)),
        Item("Cm247", div(8, 9))
    ],
    Recipe @ [Item("HEA-242")] >> [
        Item("Cm245", div(16, 9)),
        Item("Cm246", div(32, 9)),
        Item("Cm247", div(8, 9)),
        Item("Bk247", div(8, 9))
    ],

    Recipe @ [Item("LECm-243")] >> [
        Item("Cm246", div(32, 9)),
        Item("Bk247", div(16, 9)),
        Item("Bk248", div(8, 9)),
        Item("Cf249", div(8, 9)),
    ],
    Recipe @ [Item("LECm-245")] >> [
        Item("Bk247", div(40, 9)),
        Item("Bk248", div(8, 9)),
        Item("Cf249", div(4, 9)),
        Item("Cf252", div(12, 9))
    ],
    Recipe @ [Item("LECm-247")] >> [
        Item("Bk247", div(20, 9)),
        Item("Bk248", div(4, 9)),
        Item("Cf251", div(8, 9)),
        Item("Cf252", div(32, 9))
    ],
    Recipe @ [Item("HECm-243")] >> [
        Item("Cm246", div(24, 9)),
        Item("Bk247", div(24, 9)),
        Item("Bk248", div(8, 9)),
        Item("Cf249", div(8, 9))
    ],
    Recipe @ [Item("HECm-245")] >> [
        Item("Bk247", div(48, 9)),
        Item("Bk248", div(4, 9)),
        Item("Cf249", div(4, 9)),
        Item("Cf251", div(8, 9))
    ],
    Recipe @ [Item("HECm-247")] >> [
        Item("Bk248", div(8, 9)),
        Item("Cf249", div(8, 9)),
        Item("Cf251", div(24, 9)),
        Item("Cf252", div(24, 9))
    ],

    Recipe @ [Item("LEB-248")] >> [
        Item("Cf249", div(4, 9)),
        Item("Cf251", div(4, 9)),
        Item("Cf252", div(56, 9)),
    ],
    Recipe @ [Item("HEB-248")] >> [
        Item("Cf249", div(8, 9)),
        Item("Cf251", div(8, 9)),
        Item("Cf252", div(48, 9))
    ],
]

r_u = [
    Recipe @ [Item("U233", 1),  Item("U238", 8)] >>  [Item("LEU-233")],
    # Recipe @ [Item("U233", 4),  Item("U238", 5)]  >> [Item("HEU-233")],
]
r_np = [
    Recipe @ [Item("Np236", 1), Item("Np237", 8)] >> [Item("LEN-236")],
    Recipe @ [Item("Np236", 4), Item("Np237", 5)] >> [Item("HEN-236")],
]
r_pu = [
    Recipe @ [Item("Pu239", 1), Item("Pu242", 8)] >> [Item("LEP-239")],
    Recipe @ [Item("Pu241", 1), Item("Pu242", 8)] >> [Item("LEP-241")],
    Recipe @ [Item("Pu239", 4), Item("Pu242", 5)] >> [Item("HEP-239")],
    # Recipe @ [Item("Pu241", 4), Item("Pu242", 5)] >> [Item("HEP-241")],
]
r_am = [
    Recipe @ [Item("Am242", 1), Item("Am243", 8)] >> [Item("LEA-242")],
    Recipe @ [Item("Am242", 4), Item("Am243", 5)] >> [Item("HEA-242")]
]
r_cm = [
    Recipe @ [Item("Cm243", 1), Item("Cm246", 8)] >> [Item("LECm-243")],
    Recipe @ [Item("Cm245", 1), Item("Cm246", 8)] >> [Item("LECm-245")],
    Recipe @ [Item("Cm247", 1), Item("Cm246", 8)] >> [Item("LECm-247")],
    Recipe @ [Item("Cm243", 4), Item("Cm246", 5)] >> [Item("HECm-243")],
    Recipe @ [Item("Cm245", 4), Item("Cm246", 5)] >> [Item("HECm-245")],
    Recipe @ [Item("Cm247", 4), Item("Cm246", 5)] >> [Item("HECm-247")],
]
r_bk = [
    Recipe @ [Item("Bk248", 1), Item("Bk247", 8)] >> [Item("LEB-248")],
    Recipe @ [Item("Bk248", 4), Item("Bk247", 5)] >> [Item("HEB-248")]
]

out = []
for recipes in product(
    enumerate(r_u), 
    enumerate(r_np), 
    enumerate(r_pu), 
    enumerate(r_am), 
    enumerate(r_cm), 
    enumerate(r_bk)
):
    a, b = zip(*recipes)
    # print(f'Set {"".join(str(n) for n in a)}')

    out.append((a, run_recipes([*mrec, *b], inventory, p=False)))
    # print()

for a, b in out:
    print(f'Set {"".join(str(n) for n in a)}')
    run_recipes(sunnarium_recipes, b)
    print()