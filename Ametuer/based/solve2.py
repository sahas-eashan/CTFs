import base64
import base58


def solve():
    print("[*] Reading file...")
    with open("flag.txt", "r") as f:
        b64_data = "".join(
            [line.strip() for line in f if line.strip() and not line.startswith("[")]
        )

    # Layer 1: Base64
    layer1 = base64.b64decode(b64_data)
    layer1 = layer1[:-256]  # Strip padding

    # Layer 2: Base58
    layer2_bytes = base58.b58decode(layer1)

    # Layer 3: Base85 (RFC 1924)
    print("[*] Attempting Base85 (RFC 1924)...")
    try:
        # b85decode handles the characters that a85decode rejected
        layer3_bytes = base64.b85decode(layer2_bytes)
        print(f"[+] Success! Decoded {len(layer3_bytes)} bytes.")
        print(f"[+] Flag: {layer3_bytes.decode('utf-8')}")
    except Exception as e:
        print(f"[-] Base85 (RFC) failed: {e}")


if __name__ == "__main__":
    solve()
