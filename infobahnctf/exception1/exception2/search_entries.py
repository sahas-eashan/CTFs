import ast
import multiprocessing as mp
import types


def enc(value: int, start: bool = False) -> bytes:
    chunks = [0] if value == 0 else []
    tmp = value
    while tmp:
        chunks.append(tmp & 0x3F)
        tmp >>= 6
    if not chunks:
        chunks = [0]
    out = []
    for idx, chunk in enumerate(reversed(chunks)):
        byte = chunk
        if idx < len(chunks) - 1:
            byte |= 0x40
        out.append(byte)
    if start:
        out[0] |= 0x80
    return bytes(out)


def entry_bytes(start: int, end: int, target: int, depth: int = 0, lasti: bool = False) -> bytes:
    return b"".join(
        (
            enc(start // 2, True),
            enc((end - start) // 2),
            enc(target // 2),
            enc((depth << 1) | int(lasti)),
        )
    )


ORIG = ast.literal_eval.__code__
PAYLOAD = '(__import__("os").system("echo marker"),)'


def test_entry(args):
    (start, length, target, depth, lasti) = args
    table = entry_bytes(start, start + length, target, depth, lasti)
    fn = types.FunctionType(ORIG.replace(co_exceptiontable=table), ast.literal_eval.__globals__)
    try:
        res = fn(PAYLOAD)
        return args, ("ok", res)
    except Exception as exc:
        return args, ("exc", type(exc).__name__, str(exc)[:120])


def main():
    params = []
    for length in (2, 4, 6):
        for target in range(0, 232, 2):
            params.append((216, length, target, 0, False))
    ctx = mp.get_context("spawn")
    with ctx.Pool() as pool:
        for args, outcome in pool.imap_unordered(test_entry, params):
            print(args, outcome, flush=True)


if __name__ == "__main__":
    main()
