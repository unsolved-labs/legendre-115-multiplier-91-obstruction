#!/usr/bin/env python3
"""Independent SymPy replay of the cyclotomic/inertness arithmetic."""
import sympy as sp

x = sp.symbols("x")
f = x**11 + x**10 - 10*x**9 - 9*x**8 + 36*x**7 + 28*x**6 - 56*x**5 - 35*x**4 + 35*x**3 + 15*x**2 - 6*x - 1
assert sp.Poly(f, x, domain=sp.ZZ).degree() == 11
assert sp.Poly(f, x, modulus=29).is_irreducible
assert sp.n_order(29 % 23, 23) == 11
assert (12**2 + 1) % 29 == 0
assert 5**2 + 2**2 == 29
assert all((57-c) % 23 for c in (2, -2, 5, -5))
print("INDEPENDENT SYMPY REPLAY VERIFIED")
