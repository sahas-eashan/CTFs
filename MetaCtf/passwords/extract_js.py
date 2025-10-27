import urllib.request, io, pikepdf

url='https://metaproblems.com/9847c3067b5dd5d9d3220a263bd186a3/report.pdf'
data=urllib.request.urlopen(url).read()
pdf=pikepdf.open(io.BytesIO(data))
js=None
for obj in pdf.objects:
    if isinstance(obj, pikepdf.Dictionary) and '/JS' in obj:
        js=str(obj['/JS'])
        break
parts=[]
current=''
inside=False
for ch in js:
    if ch=='"':
        if inside:
            parts.append(current)
            current=''
            inside=False
        else:
            inside=True
    elif inside:
        current+=ch
print('segments',len(parts))
data=''.join(parts)
print('length',len(data))
open('payload.b64','w').write(data)
