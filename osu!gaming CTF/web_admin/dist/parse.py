import re
with open('main.js','r',encoding='utf-8') as f:
    data=f.read()
for m in re.finditer(r"localStorage\.setItem\(\"token\",([^)]*)\)", data):
    print(m.group(0))
