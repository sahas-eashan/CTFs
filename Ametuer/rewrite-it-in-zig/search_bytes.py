with open('chal','rb') as f:
    data = f.read()

for s in [b'__stack_chk_fail', b'__libc_start_main', b'syscall', b'/bin/sh', b'flag']:
    idx = data.find(s)
    print(s, hex(idx))
