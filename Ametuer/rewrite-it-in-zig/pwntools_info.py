from pwn import *

elf = ELF('chal', checksec=False)
print('arch', elf.arch)
print('bits', elf.bits)
print('entry', hex(elf.entry))
print('nx', elf.nx)
print('canary', elf.canary)
print('relro', elf.relro)
print('pie', elf.pie)
print('bss', hex(elf.bss()))
print('main', hex(elf.symbols.get('main', 0)))
