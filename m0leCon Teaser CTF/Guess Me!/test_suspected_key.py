#!/usr/bin/env python3
"""
Test the suspected key: m0leCon (key=0d8660c608d22c445d76f0992678fa60)

This got an empty/suspicious reply in a previous run, suggesting it might be correct!
"""

from pwn import *
from hashlib import sha256
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from guess_me import encrypt, BLOCK_SIZE

MESSAGE = b"next round please"
AD = b"pretty please"

def test_suspected_key():
    """Test with the suspected permutation"""
    host = "guess_me.challs.m0lecon.it"
    port = 12164

    # The suspected permutation
    perm_str = "m0leCon"
    key = bytes(sha256(perm_str.encode()).digest())[:BLOCK_SIZE]

    log.info(f"Testing suspected key: perm={perm_str}")
    log.info(f"Key: {key.hex()}")

    # Generate a fresh nonce and encrypt
    nonce = os.urandom(BLOCK_SIZE)
    ct, tag = encrypt(key, nonce, MESSAGE, AD)

    log.info(f"Nonce: {nonce.hex()}")
    log.info(f"CT: {ct.hex()}")
    log.info(f"Tag: {tag.hex()}")

    log.info(f"\nConnecting to {host}:{port}...")
    io = remote(host, port)

    # Try to complete all 5 rounds with this key
    for round_num in range(1, 6):
        log.info(f"\n{'='*60}")
        log.info(f"Round {round_num}/5")
        log.info(f"{'='*60}")

        for attempt in range(16):
            log.info(f"\n  Attempt {attempt+1}/16:")

            try:
                # Generate fresh nonce for each attempt
                nonce = os.urandom(BLOCK_SIZE)
                ct, tag = encrypt(key, nonce, MESSAGE, AD)

                # Send the payload
                io.recvuntil(b"Enter nonce (hex): ", timeout=5)
                io.sendline(nonce.hex().encode())

                io.recvuntil(b"Enter additional_data (hex): ", timeout=5)
                io.sendline(AD.hex().encode())

                io.recvuntil(b"Enter ciphertext (hex): ", timeout=5)
                io.sendline(ct.hex().encode())

                io.recvuntil(b"Enter tag (hex): ", timeout=5)
                io.sendline(tag.hex().encode())

                # Get response
                response = io.recv(timeout=2).decode(errors='ignore')
                log.info(f"    Response: {repr(response)}")

                if "There you go!" in response:
                    log.success(f"SUCCESS! Round {round_num} completed!")
                    break
                elif "Better luck next time" in response:
                    log.failure("Server rejected - round failed")
                    io.close()
                    return
                elif "Tag is invalid" in response:
                    log.warning("Tag invalid - wrong key for this round")
                    # Continue trying more attempts
                elif not response or response.strip() == "":
                    log.critical("EMPTY RESPONSE - This is suspicious!")
                    log.info("Waiting a bit to see if more data comes...")
                    try:
                        more = io.recv(timeout=3).decode(errors='ignore')
                        if more:
                            log.info(f"    More data: {repr(more)}")
                    except:
                        pass
                else:
                    log.info(f"    Unexpected: {response}")

            except EOFError:
                log.failure("Connection closed")
                return
            except Exception as e:
                log.failure(f"Error: {e}")
                import traceback
                traceback.print_exc()
                return

        # If we get here, we used all 16 attempts
        log.failure(f"Used all 16 attempts in round {round_num}")
        io.close()
        return

    # If we complete all 5 rounds
    log.success("Completed all 5 rounds! Getting flag...")
    flag = io.recvall(timeout=3).decode(errors='ignore')
    log.success(f"\n\n{'='*60}")
    log.success(f"FLAG: {flag}")
    log.success(f"{'='*60}\n")
    io.close()

if __name__ == "__main__":
    test_suspected_key()
