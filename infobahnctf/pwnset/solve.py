from pwn import *

# Connection settings
host = "pwnset.challs.infobahnc.tf"
port = 1337

context.timeout = 5  # Set 5 second timeout


def main():
    io = remote(host, port, timeout=5)
    io.interactive()


if __name__ == "__main__":
    main()
