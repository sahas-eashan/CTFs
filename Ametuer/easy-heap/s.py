import sys

# Skip the testcase count line
input()

for line in sys.stdin:
    # Parse Hex -> Bytes -> String -> Python Object (Grid)
    g = eval(bytes.fromhex(line).decode())
    
    # Identify all '1's coordinates
    s = {(r,c) for r, row in enumerate(g) for c, v in enumerate(row) if v}
    
    # Process each connected component
    while s:
        # Flood fill to find component 'q'
        q = {s.pop()}
        layer = q
        while layer:
            # Find neighbors in 's'
            layer = {n for r, c in layer for n in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)) if n in s}
            s -= layer
            q |= layer
        
        # Calculate Euler Characteristic: V - E + F
        # V = len(q)
        # E = horizontal + vertical adjacencies
        # F = 2x2 blocks
        V = len(q)
        E = sum((r+1,c) in q for r,c in q) + sum((r,c+1) in q for r,c in q)
        F = sum((r+1,c) in q and (r,c+1) in q and (r+1,c+1) in q for r,c in q)
        
        # If V - E + F <= 0, it has a hole. Change to 3.
        if V - E + F <= 0:
            for r, c in q:
                g[r][c] = 3

    # Print compact JSON
    print(str(g).replace(' ', ''))
