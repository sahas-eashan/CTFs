with open('chal','rb') as f:
    data = f.read()

rdi_ret = data.find(b'\x5f\xc3')
print('pop rdi; ret at', hex(rdi_ret))

rsi_ret = data.find(b'\x5e\xc3')
print('pop rsi; ret at', hex(rsi_ret))

rdx_ret = data.find(b'\x5a\xc3')
print('pop rdx; ret at', hex(rdx_ret))

rax_ret = data.find(b'\x58\xc3')
print('pop rax; ret at', hex(rax_ret))
