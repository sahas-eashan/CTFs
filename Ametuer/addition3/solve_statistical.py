from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
import gmpy2

# Context setup
context.log_level = 'error'  # Reduce noise

def is_perfect_cube(n):
    """Checks if n is a perfect cube."""
    root, exact = gmpy2.iroot(n, 3)
    return exact

def solve():
    # Connect to the remote instance
    # Replace HOST and PORT with actual challenge details
    # r = remote('amt.rs', 31693) 
    # For local testing with Docker:
    r = remote('localhost', 5000)

    # Known flag prefix
    flag_known = b'amateursCTF{'
    
    print(f"[*] Starting recovery. Known prefix: {flag_known}")

    # The flag length is 52 bytes (from source code assertion)
    total_length = 52

    while len(flag_known) < total_length:
        # We will binary search for the next byte (0-255)
        low = 0
        high = 255
        found_byte = None

        # Binary search for the highest byte value that keeps the message positive
        # (Guess <= Flag) -> Perfect Cube
        # (Guess > Flag)  -> Not Perfect Cube (Negative overflow wraps mod N)
        
        while low <= high:
            mid = (low + high) // 2
            
            # Construct the guess: Known parts + Current Guess Byte + Padding
            # We pad with null bytes to match the required length
            guess_bytes = flag_known + bytes([mid])
            padding_len = total_length - len(guess_bytes)
            guess_bytes += b'\x00' * padding_len
            
            # Convert to integer and shift left by 512 (as per source code)
            guess_int = bytes_to_long(guess_bytes) << 512
            
            # We send the negative of our guess as the scramble
            scramble = -guess_int

            # --- Interaction with Server ---
            # 1. Read the N and E provided by the server
            r.recvuntil(b'n, e = ')
            params = r.recvline().decode().strip()
            # The format is usually "(number, 3)"
            # We need to safely parse this tuple string
            params = params.replace('(', '').replace(')', '')
            n_str, e_str = params.split(',')
            n = int(n_str)
            
            # 2. Send the scramble
            r.recvuntil(b'scramble the flag: ')
            r.sendline(str(scramble).encode())
            
            # 3. Receive the ciphertext
            r.recvuntil(b'c = ')
            c = int(r.recvline().strip())
            # -------------------------------

            if is_perfect_cube(c):
                # If it's a perfect cube, our guess was <= the actual flag bits.
                # We try to go higher to find the exact boundary.
                found_byte = mid
                low = mid + 1
            else:
                # If not a perfect cube, our guess was > actual flag bits
                # (caused a negative wrap-around).
                high = mid - 1
                
        if found_byte is not None:
            flag_known += bytes([found_byte])
            print(f"[+] Recovered: {flag_known}")
        else:
            print("[-] Failed to recover byte. Exiting.")
            break

    print(f"\n[SUCCESS] Final Flag: {flag_known.decode()}")

if __name__ == '__main__':
    solve()
