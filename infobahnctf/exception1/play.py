import dis, types

def encode_varint(val, start=False):
    chunks=[]
    if val==0:
        chunks=[0]
    else:
        while val:
            chunks.append(val & 0x3f)
            val >>=6
    res=[]
    for i,ch in enumerate(reversed(chunks)):
        byte=ch
        if i < len(chunks)-1:
            byte |= 0x40
        res.append(byte)
    if start:
        res[0] |= 0x80
    return bytes(res)

def encode_entry(start,end,target,depth=0,lasti=False):
    data=bytearray()
    data += encode_varint(start//2, True)
    data += encode_varint((end-start)//2)
    data += encode_varint(target//2)
    data += encode_varint((depth<<1)|int(lasti))
    return bytes(data)

def foo():
    x=1
    y=2
    1/0
    return x+y

entry = encode_entry(10, 18, 20, depth=0, lasti=False)
new_code = foo.__code__.replace(co_exceptiontable=entry)
foo = types.FunctionType(new_code, globals())
print('disassembly after patch:')
print(dis.Bytecode(foo).dis())
print('exception entries', dis.Bytecode(foo).exception_entries)
print('result:', foo())
