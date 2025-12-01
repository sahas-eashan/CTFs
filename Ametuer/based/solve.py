import base64

# You may need to install the base58 library: pip install base58
import base58


def solve():
    # Read the content from the file provided in the prompt
    with open("flag.txt", "r") as f:
        # Filter out any metadata headers like if present, or just read the raw b64
        b64_data = "".join(
            [line.strip() for line in f if line.strip() and not line.startswith("[")]
        )

    # 1. Decode Base64
    try:
        decoded_layer_1 = base64.b64decode(b64_data)
    except Exception as e:
        print(f"Base64 decode failed: {e}")
        return

    # 2. Remove the trailing 0-255 byte sequence (256 bytes)
    # The challenge appends the full byte range at the end as a distractor/padding.
    ciphertext = decoded_layer_1[:-256]

    # 3. Decode Base58
    try:
        flag = base58.b58decode(ciphertext).decode("utf-8")
        print(f"Flag: {flag}")
    except Exception as e:
        print(f"Base58 decode failed: {e}")


if __name__ == "__main__":
    solve()
