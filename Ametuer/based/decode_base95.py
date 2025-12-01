import base64
import base58

# Read and decode first two layers
data = open('flag.txt', 'rb').read()
step1 = base64.b64decode(data)[:-256]
step2 = base58.b58decode(step1)

# Base95 decode (printable ASCII from 32 to 126)
def base95_decode(data):
    result = []
    num = 0
    for i, byte in enumerate(data):
        if byte < 32 or byte > 126:
            continue  # Skip non-printable
        num = num * 95 + (byte - 32)
        if (i + 1) % 5 == 0:  # Base95 encodes 4 bytes as 5 characters
            # Extract 4 bytes
            result.extend([
                (num >> 24) & 0xFF,
                (num >> 16) & 0xFF,
                (num >> 8) & 0xFF,
                num & 0xFF
            ])
            num = 0
    return bytes(result)

step3 = base95_decode(step2)
print(f'After Base95 decode: {len(step3)} bytes')
print(f'First 200 bytes: {step3[:200]}')
print()
try:
    print('As UTF-8:', step3.decode('utf-8'))
except:
    print('Not valid UTF-8')
    # Try to see if it's another base encoding
    print('As ASCII (ignore errors):', step3.decode('ascii', errors='ignore')[:300])
