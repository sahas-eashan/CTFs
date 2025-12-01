import hashlib

def solve():
    # 1. Read the ciphertext
    # The file is a hex string, so we convert it back to bytes
    with open("out.txt", "r") as f:
        ct_hex = f.read().strip()
    
    ciphertext = bytes.fromhex(ct_hex)
    
    # We know the flag is at the very end (last 47 bytes)
    # We will exclude the flag from our "whitespace check" 
    # just in case the flag actually contains spaces (unlikely, but safe).
    flag_len = 47
    data_ct = ciphertext[:-flag_len]
    
    # 2. Define Whitespace bytes
    # These are the bytes strip() would remove from os.urandom(2)
    # ASCII: \t (9), \n (10), \x0b (11), \x0c (12), \r (13), space (32)
    whitespace = {9, 10, 11, 12, 13, 32}
    
    initial_state = [None] * 32
    
    print("[*] Cracking Initial State (32 bytes)...")
    
    # 3. Crack each of the 32 bytes of the state
    for k in range(32):
        # Get every 32nd byte starting from offset k
        # These are all encrypted by the k-th byte of the state (plus round shifts)
        lane_indices = range(k, len(data_ct), 32)
        lane_ct = data_ct[k::32]
        
        candidates = []
        
        # Brute force this single byte (0-255)
        for guess in range(256):
            valid_guess = True
            
            # Check against all captured ciphertexts in this lane
            for i, idx in enumerate(lane_indices):
                # The key increments by 1 every time the stream wraps around
                # Round number is simply index // 32
                round_shift = idx // 32
                
                # Key = (BaseState + Round) % 256
                key_byte = (guess + round_shift) % 256
                
                # Plaintext = Ciphertext ^ Key
                pt_byte = lane_ct[i] ^ key_byte
                
                # CONSTRAINT: Decrypted random data cannot be whitespace
                if pt_byte in whitespace:
                    valid_guess = False
                    break
            
            if valid_guess:
                candidates.append(guess)
        
        if len(candidates) == 1:
            initial_state[k] = candidates[0]
        else:
            print(f"[!] Ambiguity at index {k}: {candidates}")
            # If ambiguous, we pick the first one, but usually, it's unique.
            initial_state[k] = candidates[0]

    print(f"[*] State Recovered: {bytes(initial_state).hex()}")

    # 4. Decrypt the Flag
    print("[*] Decrypting Flag...")
    flag_pt = []
    
    # The flag is the last 47 bytes of the full ciphertext
    start_index = len(ciphertext) - 47
    
    for i in range(47):
        abs_index = start_index + i
        ct_byte = ciphertext[abs_index]
        
        # Determine which state byte and which round applies
        state_idx = abs_index % 32
        round_shift = abs_index // 32
        
        base_key = initial_state[state_idx]
        final_key = (base_key + round_shift) % 256
        
        flag_pt.append(ct_byte ^ final_key)
        
    print("FLAG:", bytes(flag_pt).decode(errors='ignore'))

if __name__ == "__main__":
    solve()
