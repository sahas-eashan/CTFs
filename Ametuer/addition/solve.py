from pwn import *
from Crypto.Util.number import long_to_bytes

# Set to 'debug' if you want to see the raw I/O
context.log_level = "info"


def solve():
    # Connect to the challenge
    r = remote("amt.rs", 45001)

    # Parse N and e from the output: "n, e = (..., 3)"
    l = r.recvline().decode()
    if "n, e =" in l:
        # Extract the tuple part string "(123..., 3)"
        val_part = l.split("=")[1].strip()
        n, e = eval(val_part)
        log.info(f"N: {n}")
        log.info(f"e: {e}")
    else:
        log.error("Could not parse N and e")
        return

    history = []  # List of tuples: (scramble_value, ciphertext)

    log.info("Starting birthday attack... making requests.")

    # We expect a collision within roughly 400-500 requests.
    for i in range(1000):
        scramble = i

        # Interact with the server
        r.sendlineafter(b"scramble the flag: ", str(scramble).encode())
        r.recvuntil(b"c = ")
        c = int(r.recvline().strip())

        # Check the new ciphertext against all previous ciphertexts
        for S_prev, c_prev in history:
            # We want to check if these two ciphertexts correspond to the same
            # original message M.
            # c_prev = (M + S_prev)^3 % n
            # c      = (M + scramble)^3 % n

            # Let y = M + S_prev.
            # Eq 1: y^3 - c_prev = 0
            # Eq 2: (y + delta)^3 - c = 0
            # where delta = scramble - S_prev

            delta = scramble - S_prev
            c1 = c_prev
            c2 = c

            # Using the Franklin-Reiter related message logic for e=3,
            # we can derive a linear relationship to find y.
            # The polynomials are:
            # P1(y) = y^3 - c1
            # P2(y) = (y + delta)^3 - c2 = y^3 + 3*d*y^2 + 3*d^2*y + d^3 - c2

            # Subtract P2 - P1 to eliminate y^3 term:
            # Q(y) = 3*d*y^2 + 3*d^2*y + (d^3 + c1 - c2) = 0

            # Let Q(y) = A*y^2 + B*y + K
            A = (3 * delta) % n
            B = (3 * pow(delta, 2, n)) % n
            K_val = (pow(delta, 3, n) + c1 - c2) % n

            # Now we have a quadratic Q(y) = 0 and cubic P1(y) = 0.
            # Eliminate y^2:
            # Multiply Q(y) by y:  A*y^3 + B*y^2 + K*y = 0
            # Substitute y^3 = c1: A*c1  + B*y^2 + K*y = 0   (Eq 3)

            # We have:
            # Eq Q:  A*y^2 + B*y + K = 0
            # Eq 3:  B*y^2 + K*y + A*c1 = 0

            # Multiply Eq Q by B and Eq 3 by A to match the y^2 term:
            # B*A*y^2 + B^2*y + B*K = 0
            # A*B*y^2 + A*K*y + A^2*c1 = 0

            # Subtracting the two linearizes the equation:
            # (B^2 - A*K)*y + (B*K - A^2*c1) = 0
            # y = (A^2*c1 - B*K) * inverse(B^2 - A*K)

            numerator = (pow(A, 2, n) * c1 - B * K_val) % n
            denominator = (pow(B, 2, n) - A * K_val) % n

            try:
                # Calculate candidate y
                y = (numerator * pow(denominator, -1, n)) % n

                # Verify if this is actually a root
                if pow(y, 3, n) == c1:
                    log.success(
                        f"Collision found! Request {i} matches a previous request."
                    )

                    # Recover the base message M
                    # y = M + S_prev  =>  M = y - S_prev
                    M_recovered = (y - S_prev) % n

                    # The flag is in the upper bits (shifted by 256)
                    flag_int = M_recovered >> 256
                    flag = long_to_bytes(flag_int)

                    log.success(f"Flag: {flag.decode()}")
                    r.close()
                    return

            except ValueError:
                # Modular inverse failed (likely denominator is 0 mod n), just skip
                continue

        # Add current attempt to history
        history.append((scramble, c))

        if i % 20 == 0:
            log.info(f"Attempts: {i}, History size: {len(history)}")


solve()
