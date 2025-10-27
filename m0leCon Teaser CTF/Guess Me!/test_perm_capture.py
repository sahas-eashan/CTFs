# robust_send_attempt(io, nonce, ad, ct, tag)
# waits for exact prompts and prints what the server asked before sending
import time


def robust_send_attempt(io, nonce_hex, ad_hex, ct_hex, tag_hex, timeout=6):
    # Wait and print prompt for nonce
    prompt = io.recvuntil(b"Enter nonce (hex):", timeout=timeout)
    print("SERVER PROMPT:", prompt.decode(errors="replace").strip())
    io.sendline(nonce_hex.encode())

    # Wait and print prompt for additional_data
    prompt = io.recvuntil(b"Enter additional_data (hex):", timeout=timeout)
    print("SERVER PROMPT:", prompt.decode(errors="replace").strip())
    io.sendline(ad_hex.encode())

    # Wait and print prompt for ciphertext
    prompt = io.recvuntil(b"Enter ciphertext (hex):", timeout=timeout)
    print("SERVER PROMPT:", prompt.decode(errors="replace").strip())
    io.sendline(ct_hex.encode())

    # Wait and print prompt for tag
    prompt = io.recvuntil(b"Enter tag (hex):", timeout=timeout)
    print("SERVER PROMPT:", prompt.decode(errors="replace").strip())
    io.sendline(tag_hex.encode())

    # read server reply (one or more lines)
    # give server short time to respond
    time.sleep(0.05)
    out = b""
    try:
        while True:
            chunk = io.recv(timeout=0.5)
            if not chunk:
                break
            out += chunk
            # safety cap
            if len(out) > 4096:
                break
    except Exception:
        pass
    print("SERVER REPLY:", out.decode(errors="replace"))
    return out.decode(errors="replace")
