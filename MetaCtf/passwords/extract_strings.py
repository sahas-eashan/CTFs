import struct
import dnfile

with open('payload.bin','rb') as f:
    raw = f.read()
idx = raw.find(b'MZ')
if idx == -1:
    raise SystemExit('MZ not found')
pe_data = raw[idx:]
pe = dnfile.dnPE(data=pe_data)
user_strings = pe.net.user_strings

def get_method_body(method):
    rva = method.Rva
    if rva == 0:
        return b''
    offset = pe.get_offset_from_rva(rva)
    first = pe_data[offset]
    if first & 0x3 == 0x2:
        size = first >> 2
        return pe_data[offset+1:offset+1+size]
    elif first & 0x3 == 0x3:
        _, header_size = struct.unpack('<HH', pe_data[offset:offset+4])
        code_size = struct.unpack('<I', pe_data[offset+4:offset+8])[0]
        body_start = offset + header_size * 4
        return pe_data[body_start:body_start+code_size]
    return b''

for method in pe.net.mdtables.MethodDef:
    body = get_method_body(method)
    if not body:
        continue
    strings = []
    i = 0
    while i < len(body):
        opcode = body[i]
        i += 1
        if opcode == 0x72 and i + 4 <= len(body):
            token = struct.unpack('<I', body[i:i+4])[0]
            i += 4
            index = token & 0x00FFFFFF
            try:
                s = user_strings.get(index)
            except Exception:
                s = None
            if s:
                strings.append(s.value if hasattr(s, "value") else s)
        elif opcode in (0x70, 0x28, 0x73, 0x6F, 0x7B):
            i += 4
        elif opcode in (0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F,
                         0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F,
                         0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F):
            i += 4
        elif opcode in (0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D,
                         0x1E, 0x1F):
            i += 1
        elif opcode == 0xFE:
            if i < len(body):
                op2 = body[i]
                i += 1
                if op2 in (0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x09, 0x0A, 0x0B, 0x0C):
                    i += 4
        # else assume zero operand
    if strings:
        print(method.Name, '->', strings)
