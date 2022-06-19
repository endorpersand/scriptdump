"""
Feb 1, 2022
"""

from sympy import *
from sympy.vector import CoordSys3D, Point, Vector

init_printing()
N = CoordSys3D('N')
O: Point = N.origin
t = Symbol("t")

def unit_tangent(r: Vector, t: Symbol):
    v = diff(r, t)
    return simplify(v.normalize())

def unit_normal(r: Vector, t: Symbol):
    dsdt = diff(r, t).magnitude()
    T = unit_tangent(r, t)
    dTds = diff(T, t) / dsdt

    return simplify(dTds.normalize())

principal_normal = unit_normal

def binormal(r: Vector, t: Symbol):
    T = unit_tangent(r, t)
    N = unit_normal(r, t)
    return simplify(T.cross(N))

def curvature(r: Vector, t: Symbol):
    v = diff(r, t)
    a = diff(v, t)
    dsdt = v.magnitude()
    vxa = v.cross(a).magnitude()

    return simplify(vxa / dsdt ** 3)

def torsion(r: Vector, t: Symbol):
    rp1 = diff(r, t)
    rp2 = diff(rp1, t)
    rp3 = diff(rp2, t)

    n = Matrix([[x.dot(y) for x in [N.i, N.j, N.k]] for y in [rp1, rp2, rp3]]).det()
    d = rp1.cross(rp2).magnitude() ** 2

    return simplify(n / d)

r: Vector = (8 * sin(3 * t)) * N.i + (8 * cos(3 * t)) * N.j + 7 * t * N.k

print(f"""\
r: {r}

T: {unit_tangent(r, t)}
N: {unit_normal(r, t)}
B: {binormal(r, t)}

κ: {curvature(r, t)}
τ: {torsion(r, t)}
""")