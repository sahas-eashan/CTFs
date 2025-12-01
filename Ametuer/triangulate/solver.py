"""Recover the flag from the triangular LCG leak.

The script implements the approach described in README.md:
1. Build the polynomial relations that eliminate the unknown increment c.
2. Take pairwise resultants of those polynomials and gcd them to recover the prime modulus m.
3. Factor one polynomial over GF(m) to extract the linear multiplier a.
4. Solve for the increment c and, finally, the original flag value (seed).

The code defaults to the six outputs that ship with the challenge but also
accepts an optional input file with one integer per line.
"""
from __future__ import annotations

import argparse
from functools import reduce
from math import gcd
from pathlib import Path
from typing import Iterable, List

import sympy as sp
from Crypto.Util.number import inverse, long_to_bytes

HARDCODED_OUTPUTS = [
    1471207943545852478106618608447716459893047706734102352763789322304413594294954078951854930241394509747415,
    1598692736073482992170952603470306867921209728727115430390864029776876148087638761351349854291345381739153,
    7263027854980708582516705896838975362413360736887495919458129587084263748979742208194554859835570092536173,
    1421793811298953348672614691847135074360107904034360298926919347912881575026291936258693160494676689549954,
    7461500488401740536173753018264993398650307817555091262529778478859878439497126612121005384358955488744365,
    7993378969370214846258034508475124464164228761748258400865971489460388035990421363365750583336003815658573,
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Solve the triangulate challenge")
    parser.add_argument(
        "-i",
        "--inputs",
        type=Path,
        help="optional path to newline-separated outputs; defaults to the bundled leak",
    )
    return parser.parse_args()


def load_outputs(path: Path | None) -> List[int]:
    if not path:
        return HARDCODED_OUTPUTS.copy()
    data = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        data.append(int(line))
    if len(data) < 4:
        raise ValueError("Need at least four outputs to build the triangular relations")
    return data


def build_polynomials(values: List[int]) -> List[sp.Poly]:
    """Build the c-free polynomials P_j(a) described in the write-up."""
    a = sp.symbols("a")
    gaps = [idx + 2 for idx in range(len(values) - 1)]  # step sizes: 2,3,4,...
    polys: List[sp.Poly] = []
    for j in range(len(values) - 3):
        y0, y1, y2, y3 = values[j : j + 4]
        d0, d1, d2 = gaps[j], gaps[j + 1], gaps[j + 2]
        expr = y3 - (1 + a + a**d2) * y2 + (a ** (d1 + 1) + a**d1 + a) * y1 - a ** (d0 + 1) * y0
        polys.append(sp.Poly(sp.expand(expr), a))
    if len(polys) < 2:
        raise ValueError("Need at least four outputs to obtain a polynomial pair")
    return polys


def recover_modulus(polys: List[sp.Poly]) -> int:
    """Compute gcd of all pairwise resultants to isolate the prime modulus."""
    res_values: List[int] = []
    for i in range(len(polys)):
        for j in range(i + 1, len(polys)):
            res = sp.resultant(polys[i], polys[j])
            res_values.append(abs(int(res)))
    if not res_values:
        raise ValueError("Need at least two polynomials to compute resultants")
    modulus = reduce(gcd, res_values)
    if modulus <= 0:
        raise ValueError("Failed to recover a positive modulus")
    if not sp.isprime(modulus):
        raise ValueError("Recovered modulus is not prime; check the input leak")
    return modulus


def recover_multiplier(poly: sp.Poly, modulus: int) -> int:
    coeff, factors = sp.factor_list(sp.Poly(poly.as_expr(), poly.gens[0], modulus=modulus))
    for factor, _ in factors:
        if factor.degree() == 1:
            # factor is of the form u*a + v
            u, v = factor.all_coeffs()
            root = (-v * inverse(u % modulus, modulus)) % modulus
            return root
    raise ValueError("No linear factor found; unable to recover multiplier")


def recover_increment(values: List[int], modulus: int, multiplier: int) -> int:
    y1, y2 = values[0], values[1]
    numer = (y2 - pow(multiplier, 2, modulus) * y1) % modulus
    denom = (multiplier + 1) % modulus
    return (numer * inverse(denom, modulus)) % modulus


def rewind_flag(first_output: int, modulus: int, multiplier: int, increment: int) -> int:
    inv = inverse(multiplier % modulus, modulus)
    return (inv * (first_output - increment)) % modulus


def verify(values: List[int], modulus: int, multiplier: int, increment: int, flag: int) -> None:
    seed = flag
    expected_steps = [1, 2, 3, 4, 5, 6]  # cumulative triangular increments
    produced: List[int] = []
    for steps in expected_steps:
        for _ in range(steps):
            seed = (multiplier * seed + increment) % modulus
        produced.append(seed)
    if produced[: len(values)] != values:
        raise ValueError("Recovered parameters do not reproduce the provided outputs")


def main() -> None:
    args = parse_args()
    outputs = load_outputs(args.inputs)
    polys = build_polynomials(outputs)
    modulus = recover_modulus(polys)
    multiplier = recover_multiplier(polys[0], modulus)
    increment = recover_increment(outputs, modulus, multiplier)
    flag_int = rewind_flag(outputs[0], modulus, multiplier, increment)
    verify(outputs, modulus, multiplier, increment, flag_int)

    print(f"modulus (m)   = {modulus}")
    print(f"multiplier (a)= {multiplier}")
    print(f"increment (c) = {increment}")
    print(f"flag (int)    = {flag_int}")
    print(f"flag          = {long_to_bytes(flag_int).decode()}")


if __name__ == "__main__":
    main()
