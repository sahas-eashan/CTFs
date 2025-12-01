from pathlib import Path
text = Path('rendered.html').read_text(encoding='utf-16')
start = text.index('Personal page')
print(text[start:start+200])
