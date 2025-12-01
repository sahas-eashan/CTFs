try:
    import pwn
    print("pwntools available")
except ImportError as e:
    print("no pwntools", e)
