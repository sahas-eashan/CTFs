from pathlib import Path
text = Path('rendered.html').read_text(encoding='utf-16')
for i,line in enumerate(text.splitlines()):
    if '<script nonce' in line:
        print(i+1, line.strip())
