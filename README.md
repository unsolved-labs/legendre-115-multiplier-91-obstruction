# Common-multiplier 91 obstruction for binary Legendre pairs of length 115

Canonical research artifact for **Unsolved Labs R015**.

## Result

There is no binary Legendre pair of length 115 for which 91 belongs to the multiplier group of both sequences. Equivalently, after independent cyclic shifts, no such pair is fixed by decimation by 91 in both coordinates.

The complete proof is in [`THEOREM.md`](THEOREM.md), with the frozen claim in [`claim.json`](claim.json).

## Why this boundary matters

Kotsireas, Koutschan, Bulutoglu, Arquette, Turner, and Ryan performed two nonexhaustive searches for length-115 Legendre pairs whose multiplier groups both contain `{1,91}`. Their first search traversed almost 4% of a space of 3,560,597,348,629,860 cases, using about 4,359 CPU-days. Their second traversed just over 10% of a space of 3,824,345,300,380,220 cases, using about 3,436 CPU-days. The theorem here excludes the entire common-91 class without exhaustive enumeration.

Primary baseline:

- I. Kotsireas et al., *Legendre pairs of lengths ℓ ≡ 0 (mod 5)*, Special Matrices 11 (2023), 20230105, arXiv:2111.02105.
- S. M. Perera and I. S. Kotsireas, *A low-complexity algorithm to search for Legendre pairs*, Linear Algebra and its Applications 721 (2025), 149–171.
- D. Bulutoglu, D. Baczkowski, J. Yauney, *Determining the group that sends each Legendre pair to an equivalent Legendre pair*, arXiv:2604.22423 (2026).

A targeted literature audit through 2026-08-14 found no prior proof excluding the common `{1,91}` class at length 115. Independent specialist review remains pending.

## Reproduce

Python 3.12:

```bash
python verify.py
python -m pip install -r requirements.txt
python verify_sympy.py
```

Expected output:

```text
ALL COMMON-MULTIPLIER-91 ARITHMETIC OBLIGATIONS VERIFIED
INDEPENDENT SYMPY REPLAY VERIFIED
```

`verify.py` is dependency-free and uses exact integer and finite-field arithmetic. It derives the real 23rd-cyclotomic polynomial from the cyclotomic relation, independently certifies its irreducibility modulo 29 with a Rabin-style finite-field test, and checks the remaining concrete arithmetic obligations in the proof. `verify_sympy.py` provides a separate exact SymPy replay of the cyclotomic and inertness calculations.

The standard algebraic-number-theory implications connecting those obligations are stated explicitly in `THEOREM.md`; the verifier does not treat model-generated prose as an oracle.

## Files

- [`THEOREM.md`](THEOREM.md) — frozen statement and complete proof.
- [`claim.json`](claim.json) — machine-readable claim and limitation.
- [`verify.py`](verify.py) — dependency-free exact arithmetic replay.
- [`verify_sympy.py`](verify_sympy.py) — independent SymPy replay.
- [`.github/workflows/verify.yml`](.github/workflows/verify.yml) — clean-checkout CI.

## Scope

This is a structural nonexistence theorem for one symmetry class. The unrestricted existence of binary Legendre pairs of length 115 remains open.
