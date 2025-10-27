from ast import literal_eval
from math import gcd, prod

try:
    from sympy import integer_nthroot  # type: ignore
except ModuleNotFoundError:
    integer_nthroot = None


def load_data(path: str = "output.txt"):
    with open(path, "r", encoding="utf-8") as fh:
        _ = int(fh.readline().strip())  # flag length, not needed in recovery
        moduli = literal_eval(fh.readline())
        ciphertexts = literal_eval(fh.readline())
    return moduli, ciphertexts


def crt(remainders, moduli):
    total_modulus = prod(moduli)
    total = 0
    for remainder, modulus in zip(remainders, moduli):
        partial = total_modulus // modulus
        inverse = pow(partial, -1, modulus)
        total = (total + remainder * partial * inverse) % total_modulus
    return total


def exact_integer_root(power: int, value: int) -> int:
    if integer_nthroot is not None:
        root, exact = integer_nthroot(value, power)
        if not exact:
            raise ValueError("Value is not a perfect power under sympy solver.")
        return int(root)

    low, high = 0, (1 << ((value.bit_length() + power - 1) // power)) + 1
    while low < high:
        mid = (low + high) // 2
        if mid**power <= value:
            low = mid + 1
        else:
            high = mid
    candidate = low - 1
    if candidate**power != value:
        raise ValueError("Failed to extract an exact integer root.")
    return candidate


def recover_message():
    moduli, ciphertexts = load_data()

    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd(moduli[i], moduli[j]) != 1:
                raise ValueError(f"Moduli n[{i}] and n[{j}] share a factor; CRT not applicable.")

    combined = crt(ciphertexts, moduli)
    for idx, (modulus, ciphertext) in enumerate(zip(moduli, ciphertexts)):
        if combined % modulus != ciphertext:
            raise ValueError(f"CRT reconstruction failed for modulus index {idx}.")

    message_int = exact_integer_root(5, combined)
    message_bytes = message_int.to_bytes((message_int.bit_length() + 7) // 8, "big")
    return message_bytes


def main():
    message = recover_message()
    print(message.decode("utf-8"))


if __name__ == "__main__":
    main()
