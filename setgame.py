from enum import IntEnum, auto
from typing import NamedTuple
import itertools
import random

RESET = "\033[0m"
class Color(IntEnum):
    def __new__(cls, v, clr):
        o = int.__new__(cls, v)
        o._value_ = v
        o.clr = clr
        return o

    RED    = (0, "\033[31m")
    GREEN  = (1, "\033[32m")
    PURPLE = (2, "\033[35m")

class Count(IntEnum):
    ONE = 0
    TWO = auto()
    THREE = auto()

class Shape(IntEnum):
    def __new__(cls, v, *shapes):
        o = int.__new__(cls, v)
        o._value_ = v
        o.shapes = shapes
        return o

    SQUIGGLES = (0, "\u25af", "\u25af\u0338", "\u25ae")
    DIAMONDS  = (1, "\u2662", "\u2662\u0338", "\u2666")
    OVALS     = (2, "\u2b2f", "\u2b2f\u0338", "\u2b2e")

class Shading(IntEnum):
    BLANK = 0
    GRADIENT = auto()
    SOLID = auto()

class Card(NamedTuple):
    color: Color
    count: Count
    shape: Shape
    shading: Shading

    def finish_with(self, c: "Card"):
        return Card(
            *(type(a)((- a - b) % 3) for a, b in zip(self, c))
        )
    
    def __str__(self):
        return f"{self.color.clr}[" + self.shape.shapes[self.shading] * (self.count + 1) + f"]{RESET}"

def rand_cards(n=12):
    cards: "set[Card]" = set()

    while len(cards) < n:
        c = Card(
            Color(random.randrange(0, len(Color._member_names_))),
            Count(random.randrange(0, len(Count._member_names_))),
            Shape(random.randrange(0, len(Shape._member_names_))),
            Shading(random.randrange(0, len(Shading._member_names_)))
        )

        cards.add(c)
    
    return cards

def solve_board(cards: "set[Card]") -> "set[set[Card]]":
    triplets: set[set[Card]] = set()
    for c, d in itertools.combinations(cards, 2):
        if (e := c.finish_with(d)) in cards:
            t = frozenset((c,d,e))
            triplets.add(t)
    
    return triplets

def pprint_solves(solves: "set[set[Card]]"):
    for s in solves:
        print(" & ".join(str(c) for c in s))

if __name__ == "__main__":
    cards = {
        Card(Color.GREEN,  Count.TWO,   Shape.SQUIGGLES, Shading.GRADIENT),
        Card(Color.GREEN,  Count.THREE, Shape.SQUIGGLES, Shading.GRADIENT),
        Card(Color.GREEN,  Count.THREE, Shape.OVALS,     Shading.BLANK),
        Card(Color.RED,    Count.ONE,   Shape.OVALS,     Shading.BLANK),
        Card(Color.GREEN,  Count.ONE,   Shape.OVALS,     Shading.BLANK),
        Card(Color.RED,    Count.TWO,   Shape.OVALS,     Shading.BLANK),
        Card(Color.GREEN,  Count.ONE,   Shape.SQUIGGLES, Shading.BLANK),
        Card(Color.PURPLE, Count.THREE, Shape.DIAMONDS,  Shading.BLANK),
        Card(Color.RED,    Count.THREE, Shape.DIAMONDS,  Shading.GRADIENT),
        Card(Color.RED,    Count.THREE, Shape.SQUIGGLES, Shading.BLANK),
        Card(Color.PURPLE, Count.TWO,   Shape.OVALS,     Shading.SOLID),
        Card(Color.GREEN,  Count.THREE, Shape.DIAMONDS,  Shading.SOLID),
    }

    pprint_solves(solve_board(cards))