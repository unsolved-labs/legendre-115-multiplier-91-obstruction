#!/usr/bin/env python3
"""Dependency-free exact replay for the common-multiplier-91 obstruction.

The script checks the concrete arithmetic obligations in THEOREM.md using only
integer and finite-field arithmetic. Standard theorem-level implications
(multiplier normalization, ideal factorization, Kronecker's theorem) remain
visible in the written proof rather than hidden in a solver.
"""

from math import gcd

P = 29


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def trim(a):
    a = [x % P for x in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def poly_add(a, b):
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % P
    return trim(out)


def poly_sub(a, b):
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % P
    return trim(out)


def poly_mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % P
    return trim(out)


def poly_divmod(a, b):
    a = trim(a[:])
    b = trim(b[:])
    require(b != [0], "division by zero polynomial")
    q = [0] * max(1, len(a) - len(b) + 1)
    inv = pow(b[-1], -1, P)
    while len(a) >= len(b) and a != [0]:
        d = len(a) - len(b)
        c = a[-1] * inv % P
        q[d] = c
        for j in range(len(b)):
            a[d + j] = (a[d + j] - c * b[j]) % P
        a = trim(a)
    return trim(q), trim(a)


def poly_mod(a, f):
    return poly_divmod(a, f)[1]


def poly_gcd(a, b):
    a, b = trim(a), trim(b)
    while b != [0]:
        _, r = poly_divmod(a, b)
        a, b = b, r
    if a == [0]:
        return [0]
    inv = pow(a[-1], -1, P)
    return trim([(c * inv) % P for c in a])


def poly_pow_mod(base, exponent, f):
    result = [1]
    base = poly_mod(base, f)
    while exponent:
        if exponent & 1:
            result = poly_mod(poly_mul(result, base), f)
        base = poly_mod(poly_mul(base, base), f)
        exponent >>= 1
    return result


def mul_order(a, n):
    require(gcd(a, n) == 1, "order input is not a unit")
    x = 1
    for k in range(1, n + 1):
        x = x * a % n
        if x == 1:
            return k
    raise AssertionError("order not found")


def zpoly_add(a, b):
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def zpoly_mul_x(a):
    return [0] + a


def zpoly_sub(a, b):
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = (a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def main():
    ell, m, q = 115, 91, 23
    support, lam, fiber = 57, 56, 5

    require(gcd(58, ell) == 1, "normalization gcd")
    require(gcd(m, ell) == 1, "91 must be a unit")
    require(m * m % ell == 1, "91 must be an involution")
    require(m % q == q - 1, "91 must reduce to -1 modulo 23")

    nonzero = fiber * lam
    zero = 2 * support + (fiber - 1) * lam
    require((zero, nonzero) == (338, 280), "compression constants")
    require(zero % 2 == nonzero % 2 == 0, "parity constants")
    require(sorted(2 * j % q for j in range(q)) == list(range(q)), "Frobenius injectivity")

    uv0, uv1 = zero // 2, nonzero // 2
    require((uv0, uv1) == (169, 140), "u/v correlations")
    require(uv0 - uv1 == 29, "Fourier norm equation")

    require(29 % 23 == 6 and mul_order(6, 23) == 11, "residue degree")
    require(all(pow(6, k, 23) != 22 for k in range(1, 11)), "no smaller -1 power")

    # Derive the degree-11 polynomial of t=zeta+zeta^{-1} from
    # 1 + sum_{k=1}^{11}(zeta^k+zeta^{-k}) = 0.
    S0, S1 = [2], [0, 1]
    S = [S0, S1]
    for _k in range(2, 12):
        S.append(zpoly_sub(zpoly_mul_x(S[-1]), S[-2]))
    F = [1]
    for k in range(1, 12):
        F = zpoly_add(F, S[k])
    expected_high_to_low = [1, 1, -10, -9, 36, 28, -56, -35, 35, 15, -6, -1]
    expected = list(reversed(expected_high_to_low))
    require(F == expected, "real cyclotomic polynomial derivation")

    # Degree 11 is prime. Rabin irreducibility criterion reduces to:
    # x^(29^11)=x mod F and gcd(F, x^29-x)=1.
    f = [c % P for c in expected]
    xpoly = [0, 1]
    require(poly_pow_mod(xpoly, P**11, f) == xpoly, "Frobenius 11 fixed-point test")
    g = poly_gcd(f, poly_sub(poly_pow_mod(xpoly, P, f), xpoly))
    require(g == [1], "degree-1 factor exclusion")

    require((12 * 12 + 1) % 29 == 0, "-1 square mod 29")
    require(5 * 5 + 2 * 2 == 29, "Gaussian norm")
    require(29**11 == (5 * 5 + 2 * 2)**11, "absolute ideal norm arithmetic")

    require(22 < 44, "primitive 92nd root degree obstruction")
    require((23**21) % 2 == 1, "Q(zeta_23) unramified-at-2 discriminant input")
    require((-4) % 2 == 0, "Q(i) ramified-at-2 discriminant input")

    candidates = [2, -2, 5, -5]
    require(57 % 23 == 11, "final residue")
    require(all((57 - c) % 23 != 0 for c in candidates), "final cyclotomic contradiction")

    print("ALL COMMON-MULTIPLIER-91 ARITHMETIC OBLIGATIONS VERIFIED")


if __name__ == "__main__":
    main()
