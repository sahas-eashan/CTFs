from pathlib import Path
text = Path('rendered.html').read_text(encoding='utf-16')
marker = 'MARKER'
start = text.index(marker)
script_idx = text.index('<script nonce=')
segment = text[start:script_idx]
print('segment length', len(segment))
print('double quotes', segment.count('"'))
print('single quotes', segment.count("'"))
