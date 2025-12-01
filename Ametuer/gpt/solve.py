import base64

def solve_stego(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # We only care about the Base64 lines (lines 1-161 in your file)
    # The rest is the "decoded" text which we can ignore for extraction.
    b64_lines = [line.strip() for line in lines if line.strip() and not line.startswith('[source')]

    binary_string = ""
    
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    for line in b64_lines:
        if line.endswith('=='):
            # 2 padding chars = 4 bits hidden in the char before '=='
            last_char = line[-3]
            val = base64_chars.index(last_char)
            # Extract last 4 bits
            bits = format(val, '06b')[-4:]
            binary_string += bits
            
        elif line.endswith('='):
            # 1 padding char = 2 bits hidden in the char before '='
            last_char = line[-2]
            val = base64_chars.index(last_char)
            # Extract last 2 bits
            bits = format(val, '06b')[-2:]
            binary_string += bits

    # Convert binary string to ASCII
    flag = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        if len(byte) == 8:
            flag += chr(int(byte, 2))
            
    return flag

# Run the solver
# Note: Ensure 'chall.txt' contains the Base64 lines provided in the prompt
print(solve_stego('chall.txt'))