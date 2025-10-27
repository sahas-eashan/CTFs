import json
import re
from pathlib import Path

text = Path('ine_exiftool.html').read_text(encoding='utf-8')
match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', text, re.S)
if not match:
    raise SystemExit('script not found')
data = json.loads(match.group(1))
body = data['props']['pageProps']['blogPostsById']['postBody']['text']
for line in body.splitlines():
    if 'system(' in line:
        print(line.encode('utf-8'))
