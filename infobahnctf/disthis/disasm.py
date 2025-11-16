import marshal, types, dis, sys, io, os, struct

PYC_PATH = os.path.join(os.path.dirname(__file__), "output.pyc")


def load_code_from_pyc(path: str):
    with open(path, "rb") as f:
        data = f.read()
    # Try a few common header lengths (PEP 552 variations)
    for header_len in (16, 12, 8):
        try:
            co = marshal.loads(data[header_len:])
            if isinstance(co, types.CodeType):
                return co, header_len
        except Exception:
            continue
    raise RuntimeError(
        "Failed to parse code object from pyc; unsupported header format"
    )


def walk_code_objects(co: types.CodeType):
    # recursively yield code objects
    yield co
    for const in co.co_consts:
        if isinstance(const, types.CodeType):
            yield from walk_code_objects(const)


def dump_consts(name: str, co: types.CodeType):
    consts = co.co_consts
    print(f"[i] {name}: {len(consts)} constants")
    type_counts = {}
    for c in consts:
        type_counts[type(c).__name__] = type_counts.get(type(c).__name__, 0) + 1
    print("    types:", type_counts)
    strs = [c for c in consts if isinstance(c, str)]
    ints = [c for c in consts if isinstance(c, int)]
    tuples = [c for c in consts if isinstance(c, tuple)]
    dicts = [c for c in consts if isinstance(c, dict)]
    lists = [c for c in consts if isinstance(c, list)]
    if strs:
        print(f"    sample strings ({min(10, len(strs))}):", strs[:10])
    if ints:
        print(f"    sample ints ({min(10, len(ints))}):", ints[:10])
    if tuples:
        print(
            f"    found {len(tuples)} tuple consts; sizes:",
            [len(t) for t in tuples[:5]],
        )
    if dicts:
        print(
            f"    found {len(dicts)} dict consts; sizes:", [len(d) for d in dicts[:5]]
        )
    if lists:
        print(
            f"    found {len(lists)} list consts; sizes:", [len(l) for l in lists[:5]]
        )


def main():
    co, header_len = load_code_from_pyc(PYC_PATH)
    print(f"[i] Loaded code object from {PYC_PATH} (skipped {header_len} header bytes)")

    # Avoid full disassembly since the code object seems intentionally hostile to dis
    try:
        print("\n[i] Quick disassembly preview (may fail):")
        dis.dis(co)
    except Exception as e:
        print(f"[i] Disassembly failed as expected: {e.__class__.__name__}: {e}")

    print("\n[i] Dumping constant pools:")
    dump_consts("top-level", co)
    for idx, sub in enumerate(
        [c for c in co.co_consts if isinstance(c, types.CodeType)]
    ):
        dump_consts(f"code const {idx} ({sub.co_name})", sub)

    # Heuristic: collect all 1-char strings and any following ints from bytecode stream order
    # If mapping index->char exists in consts, reconstruct string by ordered indices
    consts = co.co_consts
    one_char = [s for s in consts if isinstance(s, str) and len(s) == 1]
    printable = set("\n\r\t")
    printable.update(chr(i) for i in range(32, 127))
    char_set = set(one_char)
    if char_set:
        print(f"\n[i] Found {len(char_set)} unique single-char strings.")
    # Attempt to find a dict/tuple mapping
    possible_maps = []
    for obj in consts:
        if (
            isinstance(obj, (tuple, list))
            and obj
            and all(isinstance(x, (tuple, list)) and len(x) == 2 for x in obj)
        ):
            if all(
                (isinstance(a, str) and isinstance(b, int))
                or (isinstance(a, int) and isinstance(b, str))
                for a, b in obj
            ):
                possible_maps.append(obj)
        if isinstance(obj, dict) and obj:
            if all(
                (isinstance(k, (int, str)) and isinstance(v, (int, str)))
                for k, v in obj.items()
            ):
                possible_maps.append(obj)
    print(f"[i] Possible key-value mappings found: {len(possible_maps)}")
    for m in possible_maps[:3]:
        print(
            "    example mapping size:",
            len(m) if not isinstance(m, dict) else len(m.keys()),
        )

    # Try reconstruct by pairing sequential (char, int) in consts order
    pairs = []
    prev = None
    for c in consts:
        if isinstance(c, str) and len(c) == 1:
            prev = c
        elif isinstance(c, int) and prev is not None:
            pairs.append((prev, c))
            prev = None
    if pairs:
        print(
            f"[i] Heuristic char->pos pairs found: {len(pairs)} (showing first 10):",
            pairs[:10],
        )
        # Normalize positions to start at 0
        min_pos = min(p for _, p in pairs)
        mapping = {p - min_pos: ch for ch, p in pairs}
        # Reconstruct string by sequential indices until gap
        out = []
        i = 0
        while i in mapping:
            out.append(mapping[i])
            i += 1
        candidate = "".join(out)
        print("[i] Reconstructed (normalized) string prefix:", candidate[:120])
        # If it looks like a flag, print fully
        if "{" in candidate and "}" in candidate:
            print("[FLAG?]", candidate)

    # New: Parse LOAD_CONST instruction stream to pair (char, pos)
    def reconstruct_from_instructions(code: types.CodeType, label: str):
        print(f"\n[i] Scanning bytecode for (char, pos) LOAD_CONST pairs in {label}...")
        mapping = {}
        count_pairs = 0
        prev_char = None
        yielded = 0
        try:
            bc = dis.Bytecode(code)
            for ins in bc:
                # Only consider LOAD_CONST
                if ins.opname != "LOAD_CONST":
                    continue
                val = ins.argval
                if isinstance(val, str) and len(val) == 1:
                    prev_char = val
                elif isinstance(val, int) and prev_char is not None:
                    # record position -> char
                    mapping[val] = prev_char
                    count_pairs += 1
                    prev_char = None
                yielded += 1
        except Exception as e:
            print(f"[i] Bytecode iteration interrupted: {e.__class__.__name__}: {e}")
        if count_pairs:
            print(f"[i] Collected {count_pairs} (char, pos) pairs from instructions.")
            # Normalize and reconstruct by sorted position
            positions = sorted(mapping.keys())
            # Some challenges offset positions; normalize to start at 0
            if positions:
                offset = positions[0]
                normalized = {p - offset: ch for p, ch in mapping.items()}
                out = "".join(ch for _, ch in sorted(normalized.items()))
                print("[i] Reconstructed from LOAD_CONST (normalized):", out[:200])
                if "{" in out and "}" in out:
                    print("[FLAG?]", out)
            # Also try without normalization (absolute positions)
            abs_out = "".join(ch for _, ch in sorted(mapping.items()))
            if abs_out:
                print("[i] Reconstructed from LOAD_CONST (absolute):", abs_out[:200])
                if "{" in abs_out and "}" in abs_out:
                    print("[FLAG?]", abs_out)
        else:
            print("[i] No (char, pos) pairs found in instruction stream.")

    reconstruct_from_instructions(co, "top-level")
    for idx, sub in enumerate(
        [c for c in co.co_consts if isinstance(c, types.CodeType)]
    ):
        reconstruct_from_instructions(sub, f"code const {idx} ({sub.co_name})")

    # Fallback: Parse raw bytecode to avoid dis iterator failures
    def reconstruct_from_bytes(code: types.CodeType, label: str):
        print(f"\n[i] Scanning raw co_code for LOAD_CONST pairs in {label}...")
        try:
            EXT = dis.opmap.get("EXTENDED_ARG")
            LOAD = dis.opmap.get("LOAD_CONST")
        except Exception:
            EXT = None
            LOAD = None
        bytecode = code.co_code
        mapping = {}
        prev_char = None
        ext = 0
        i = 0
        n = len(bytecode)
        while i + 1 < n:
            op = bytecode[i]
            arg = bytecode[i + 1]
            if EXT is not None and op == EXT:
                ext = (ext << 8) | arg
            else:
                full_arg = arg | (ext << 8)
                ext = 0
                if LOAD is not None and op == LOAD:
                    if 0 <= full_arg < len(code.co_consts):
                        val = code.co_consts[full_arg]
                    else:
                        val = None
                    if isinstance(val, str) and len(val) == 1:
                        prev_char = val
                    elif isinstance(val, int) and prev_char is not None:
                        mapping[val] = prev_char
                        prev_char = None
            i += 2
        if mapping:
            print(f"[i] Collected {len(mapping)} pairs from raw bytes.")
            positions = sorted(mapping.keys())
            if positions:
                offset = positions[0]
                normalized = {p - offset: ch for p, ch in mapping.items()}
                out = "".join(ch for _, ch in sorted(normalized.items()))
                print("[i] Bytes-based reconstruction (normalized):", out[:200])
                if "{" in out and "}" in out:
                    print("[FLAG?]", out)
            abs_out = "".join(ch for _, ch in sorted(mapping.items()))
            if abs_out:
                print("[i] Bytes-based reconstruction (absolute):", abs_out[:200])
                if "{" in abs_out and "}" in abs_out:
                    print("[FLAG?]", abs_out)
        else:
            print("[i] No pairs found from raw bytes.")

    reconstruct_from_bytes(co, "top-level")

    # As a last resort, try executing (may crash intentionally)
    try:
        print("\n[i] Attempting to execute module in isolated globals...")
        g = {"__name__": "__main__"}
        exec(co, g)
    except Exception as e:
        print(f"[i] Execution raised: {e.__class__.__name__}: {e}")


if __name__ == "__main__":
    main()
