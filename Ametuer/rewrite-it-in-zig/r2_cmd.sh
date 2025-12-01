#!/bin/sh
cd /mnt/c/Users/Cyborg/Documents/GitHub/CTFs/Ametuer/rewrite-it-in-zig
r2 -b 64 -a x86 -q -c 's 0x1034540;pd 30' chal
