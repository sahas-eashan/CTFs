#!/usr/bin/env python3

# Find x86 instructions whose mnemonics contain the allowed strings
ALLOWED_MNEMONICS = ["jmp", "add", "mov", "sub", "inc", "dec", "cmp", "push", "pop", "int3"]

# Common x86 mnemonics
all_mnemonics = [
    "adc", "add", "and", "bsf", "bsr", "bswap", "bt", "btc", "btr", "bts",
    "call", "cbw", "cdq", "clc", "cld", "cli", "cmc", "cmova", "cmovae",
    "cmovb", "cmovbe", "cmovc", "cmove", "cmovg", "cmovge", "cmovl", "cmovle",
    "cmovna", "cmovnae", "cmovnb", "cmovnbe", "cmovnc", "cmovne", "cmovng",
    "cmovnge", "cmovnl", "cmovnle", "cmovno", "cmovnp", "cmovns", "cmovnz",
    "cmovo", "cmovp", "cmovpe", "cmovpo", "cmovs", "cmovz", "cmp", "cmps",
    "cmpsb", "cmpsd", "cmpsw", "cmpxchg", "cmpxchg8b", "cpuid", "cwd", "cwde",
    "daa", "das", "dec", "div", "enter", "hlt", "idiv", "imul", "in", "inc",
    "ins", "insb", "insd", "insw", "int", "int3", "into", "invd", "invlpg",
    "iret", "iretd", "ja", "jae", "jb", "jbe", "jc", "jcxz", "je", "jecxz",
    "jg", "jge", "jl", "jle", "jmp", "jna", "jnae", "jnb", "jnbe", "jnc",
    "jne", "jng", "jnge", "jnl", "jnle", "jno", "jnp", "jns", "jnz", "jo",
    "jp", "jpe", "jpo", "js", "jz", "lahf", "lar", "lds", "lea", "leave",
    "les", "lfs", "lgdt", "lgs", "lidt", "lldt", "lmsw", "lock", "lods",
    "lodsb", "lodsd", "lodsw", "loop", "loope", "loopne", "lsl", "lss", "ltr",
    "mov", "movs", "movsb", "movsd", "movsw", "movsx", "movzx", "mul", "neg",
    "nop", "not", "or", "out", "outs", "outsb", "outsd", "outsw", "pop",
    "popa", "popad", "popf", "popfd", "push", "pusha", "pushad", "pushf",
    "pushfd", "rcl", "rcr", "rdmsr", "rdpmc", "rdtsc", "rep", "repe", "repne",
    "repnz", "repz", "ret", "retf", "rol", "ror", "rsm", "sahf", "sal", "sar",
    "sbb", "scas", "scasb", "scasd", "scasw", "seta", "setae", "setb", "setbe",
    "setc", "sete", "setg", "setge", "setl", "setle", "setna", "setnae",
    "setnb", "setnbe", "setnc", "setne", "setng", "setnge", "setnl", "setnle",
    "setno", "setnp", "setns", "setnz", "seto", "setp", "setpe", "setpo",
    "sets", "setz", "sgdt", "shl", "shld", "shr", "shrd", "sidt", "sldt",
    "smsw", "stc", "std", "sti", "stos", "stosb", "stosd", "stosw", "str",
    "sub", "test", "verr", "verw", "wait", "wbinvd", "wrmsr", "xadd", "xchg",
    "xlat", "xlatb", "xor",
    # Some with prefixes
    "movabs", "movsd", "movss", "movups", "movaps",
    "addsd", "addss", "addps", "addpd",
    "subsd", "subss", "subps", "subpd",
    "cmpsd", "cmpss", "cmpps", "cmppd",
    "pushw", "pushd",
    "popw", "popd",
]

print("Instructions that would pass the filter:")
print("=" * 50)

for mnemonic in all_mnemonics:
    if any(part in mnemonic for part in ALLOWED_MNEMONICS):
        print(f"  {mnemonic}")

print("\n" + "=" * 50)
print("\nInteresting ones:")
print("  - cmov* instructions (conditional moves)")
print("  - movs, movsb, movsd, movsw (string moves)")
print("  - movsx, movzx (move with sign/zero extend)")
print("  - movabs (move absolute)")
print("  - rep/repz/repne (prefix for sub operations like 'rep movsb')")
print("  - push*, pop* variants")
print("  - add*, sub* with SSE")
print("\nMost importantly:")
print("  - 'cmps' contains 'cmp' - compare strings")
print("  - 'popa'/'popad' contains 'pop' - pop all registers!")
print("  - 'pusha'/'pushad' contains 'push' - push all registers!")
print("  - 'movs' contains 'mov' - move string data")
