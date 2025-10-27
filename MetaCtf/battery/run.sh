#!/bin/sh
socat tcp-l:1337,reuseaddr,fork EXEC:"/opt/entrypoint.sh",pty,stderr