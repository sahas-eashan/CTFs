
/mnt/c/Users/Cyborg/Documents/GitHub/CTFs/infobahnctf/Risk/risky:     file format elf64-x86-64


Disassembly of section .init:

0000000000001000 <_init>:
    1000:	f3 0f 1e fa          	endbr64
    1004:	48 83 ec 08          	sub    rsp,0x8
    1008:	48 8b 05 e1 3f 00 00 	mov    rax,QWORD PTR [rip+0x3fe1]        # 4ff0 <__gmon_start__@Base>
    100f:	48 85 c0             	test   rax,rax
    1012:	74 02                	je     1016 <_init+0x16>
    1014:	ff d0                	call   rax
    1016:	48 83 c4 08          	add    rsp,0x8
    101a:	c3                   	ret

Disassembly of section .plt:

0000000000001020 <.plt>:
    1020:	ff 35 e2 3e 00 00    	push   QWORD PTR [rip+0x3ee2]        # 4f08 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026:	ff 25 e4 3e 00 00    	jmp    QWORD PTR [rip+0x3ee4]        # 4f10 <_GLOBAL_OFFSET_TABLE_+0x10>
    102c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    1030:	f3 0f 1e fa          	endbr64
    1034:	68 00 00 00 00       	push   0x0
    1039:	e9 e2 ff ff ff       	jmp    1020 <_init+0x20>
    103e:	66 90                	xchg   ax,ax
    1040:	f3 0f 1e fa          	endbr64
    1044:	68 01 00 00 00       	push   0x1
    1049:	e9 d2 ff ff ff       	jmp    1020 <_init+0x20>
    104e:	66 90                	xchg   ax,ax
    1050:	f3 0f 1e fa          	endbr64
    1054:	68 02 00 00 00       	push   0x2
    1059:	e9 c2 ff ff ff       	jmp    1020 <_init+0x20>
    105e:	66 90                	xchg   ax,ax
    1060:	f3 0f 1e fa          	endbr64
    1064:	68 03 00 00 00       	push   0x3
    1069:	e9 b2 ff ff ff       	jmp    1020 <_init+0x20>
    106e:	66 90                	xchg   ax,ax
    1070:	f3 0f 1e fa          	endbr64
    1074:	68 04 00 00 00       	push   0x4
    1079:	e9 a2 ff ff ff       	jmp    1020 <_init+0x20>
    107e:	66 90                	xchg   ax,ax
    1080:	f3 0f 1e fa          	endbr64
    1084:	68 05 00 00 00       	push   0x5
    1089:	e9 92 ff ff ff       	jmp    1020 <_init+0x20>
    108e:	66 90                	xchg   ax,ax
    1090:	f3 0f 1e fa          	endbr64
    1094:	68 06 00 00 00       	push   0x6
    1099:	e9 82 ff ff ff       	jmp    1020 <_init+0x20>
    109e:	66 90                	xchg   ax,ax
    10a0:	f3 0f 1e fa          	endbr64
    10a4:	68 07 00 00 00       	push   0x7
    10a9:	e9 72 ff ff ff       	jmp    1020 <_init+0x20>
    10ae:	66 90                	xchg   ax,ax
    10b0:	f3 0f 1e fa          	endbr64
    10b4:	68 08 00 00 00       	push   0x8
    10b9:	e9 62 ff ff ff       	jmp    1020 <_init+0x20>
    10be:	66 90                	xchg   ax,ax
    10c0:	f3 0f 1e fa          	endbr64
    10c4:	68 09 00 00 00       	push   0x9
    10c9:	e9 52 ff ff ff       	jmp    1020 <_init+0x20>
    10ce:	66 90                	xchg   ax,ax
    10d0:	f3 0f 1e fa          	endbr64
    10d4:	68 0a 00 00 00       	push   0xa
    10d9:	e9 42 ff ff ff       	jmp    1020 <_init+0x20>
    10de:	66 90                	xchg   ax,ax
    10e0:	f3 0f 1e fa          	endbr64
    10e4:	68 0b 00 00 00       	push   0xb
    10e9:	e9 32 ff ff ff       	jmp    1020 <_init+0x20>
    10ee:	66 90                	xchg   ax,ax
    10f0:	f3 0f 1e fa          	endbr64
    10f4:	68 0c 00 00 00       	push   0xc
    10f9:	e9 22 ff ff ff       	jmp    1020 <_init+0x20>
    10fe:	66 90                	xchg   ax,ax
    1100:	f3 0f 1e fa          	endbr64
    1104:	68 0d 00 00 00       	push   0xd
    1109:	e9 12 ff ff ff       	jmp    1020 <_init+0x20>
    110e:	66 90                	xchg   ax,ax
    1110:	f3 0f 1e fa          	endbr64
    1114:	68 0e 00 00 00       	push   0xe
    1119:	e9 02 ff ff ff       	jmp    1020 <_init+0x20>
    111e:	66 90                	xchg   ax,ax
    1120:	f3 0f 1e fa          	endbr64
    1124:	68 0f 00 00 00       	push   0xf
    1129:	e9 f2 fe ff ff       	jmp    1020 <_init+0x20>
    112e:	66 90                	xchg   ax,ax
    1130:	f3 0f 1e fa          	endbr64
    1134:	68 10 00 00 00       	push   0x10
    1139:	e9 e2 fe ff ff       	jmp    1020 <_init+0x20>
    113e:	66 90                	xchg   ax,ax
    1140:	f3 0f 1e fa          	endbr64
    1144:	68 11 00 00 00       	push   0x11
    1149:	e9 d2 fe ff ff       	jmp    1020 <_init+0x20>
    114e:	66 90                	xchg   ax,ax
    1150:	f3 0f 1e fa          	endbr64
    1154:	68 12 00 00 00       	push   0x12
    1159:	e9 c2 fe ff ff       	jmp    1020 <_init+0x20>
    115e:	66 90                	xchg   ax,ax
    1160:	f3 0f 1e fa          	endbr64
    1164:	68 13 00 00 00       	push   0x13
    1169:	e9 b2 fe ff ff       	jmp    1020 <_init+0x20>
    116e:	66 90                	xchg   ax,ax
    1170:	f3 0f 1e fa          	endbr64
    1174:	68 14 00 00 00       	push   0x14
    1179:	e9 a2 fe ff ff       	jmp    1020 <_init+0x20>
    117e:	66 90                	xchg   ax,ax
    1180:	f3 0f 1e fa          	endbr64
    1184:	68 15 00 00 00       	push   0x15
    1189:	e9 92 fe ff ff       	jmp    1020 <_init+0x20>
    118e:	66 90                	xchg   ax,ax
    1190:	f3 0f 1e fa          	endbr64
    1194:	68 16 00 00 00       	push   0x16
    1199:	e9 82 fe ff ff       	jmp    1020 <_init+0x20>
    119e:	66 90                	xchg   ax,ax
    11a0:	f3 0f 1e fa          	endbr64
    11a4:	68 17 00 00 00       	push   0x17
    11a9:	e9 72 fe ff ff       	jmp    1020 <_init+0x20>
    11ae:	66 90                	xchg   ax,ax

Disassembly of section .plt.got:

00000000000011b0 <__cxa_finalize@plt>:
    11b0:	f3 0f 1e fa          	endbr64
    11b4:	ff 25 1e 3e 00 00    	jmp    QWORD PTR [rip+0x3e1e]        # 4fd8 <__cxa_finalize@GLIBC_2.2.5>
    11ba:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .plt.sec:

00000000000011c0 <setvbuf@plt>:
    11c0:	f3 0f 1e fa          	endbr64
    11c4:	ff 25 4e 3d 00 00    	jmp    QWORD PTR [rip+0x3d4e]        # 4f18 <setvbuf@GLIBC_2.2.5>
    11ca:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000011d0 <printf@plt>:
    11d0:	f3 0f 1e fa          	endbr64
    11d4:	ff 25 46 3d 00 00    	jmp    QWORD PTR [rip+0x3d46]        # 4f20 <printf@GLIBC_2.2.5>
    11da:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000011e0 <sprintf@plt>:
    11e0:	f3 0f 1e fa          	endbr64
    11e4:	ff 25 3e 3d 00 00    	jmp    QWORD PTR [rip+0x3d3e]        # 4f28 <sprintf@GLIBC_2.2.5>
    11ea:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000011f0 <strchr@plt>:
    11f0:	f3 0f 1e fa          	endbr64
    11f4:	ff 25 36 3d 00 00    	jmp    QWORD PTR [rip+0x3d36]        # 4f30 <strchr@GLIBC_2.2.5>
    11fa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001200 <strlen@plt>:
    1200:	f3 0f 1e fa          	endbr64
    1204:	ff 25 2e 3d 00 00    	jmp    QWORD PTR [rip+0x3d2e]        # 4f38 <strlen@GLIBC_2.2.5>
    120a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001210 <strncmp@plt>:
    1210:	f3 0f 1e fa          	endbr64
    1214:	ff 25 26 3d 00 00    	jmp    QWORD PTR [rip+0x3d26]        # 4f40 <strncmp@GLIBC_2.2.5>
    121a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001220 <memset@plt>:
    1220:	f3 0f 1e fa          	endbr64
    1224:	ff 25 1e 3d 00 00    	jmp    QWORD PTR [rip+0x3d1e]        # 4f48 <memset@GLIBC_2.2.5>
    122a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001230 <strncat@plt>:
    1230:	f3 0f 1e fa          	endbr64
    1234:	ff 25 16 3d 00 00    	jmp    QWORD PTR [rip+0x3d16]        # 4f50 <strncat@GLIBC_2.2.5>
    123a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001240 <memcpy@plt>:
    1240:	f3 0f 1e fa          	endbr64
    1244:	ff 25 0e 3d 00 00    	jmp    QWORD PTR [rip+0x3d0e]        # 4f58 <memcpy@GLIBC_2.14>
    124a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001250 <time@plt>:
    1250:	f3 0f 1e fa          	endbr64
    1254:	ff 25 06 3d 00 00    	jmp    QWORD PTR [rip+0x3d06]        # 4f60 <time@GLIBC_2.2.5>
    125a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001260 <strcpy@plt>:
    1260:	f3 0f 1e fa          	endbr64
    1264:	ff 25 fe 3c 00 00    	jmp    QWORD PTR [rip+0x3cfe]        # 4f68 <strcpy@GLIBC_2.2.5>
    126a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001270 <__isoc99_sscanf@plt>:
    1270:	f3 0f 1e fa          	endbr64
    1274:	ff 25 f6 3c 00 00    	jmp    QWORD PTR [rip+0x3cf6]        # 4f70 <__isoc99_sscanf@GLIBC_2.7>
    127a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001280 <fclose@plt>:
    1280:	f3 0f 1e fa          	endbr64
    1284:	ff 25 ee 3c 00 00    	jmp    QWORD PTR [rip+0x3cee]        # 4f78 <fclose@GLIBC_2.2.5>
    128a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001290 <__stack_chk_fail@plt>:
    1290:	f3 0f 1e fa          	endbr64
    1294:	ff 25 e6 3c 00 00    	jmp    QWORD PTR [rip+0x3ce6]        # 4f80 <__stack_chk_fail@GLIBC_2.4>
    129a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000012a0 <__isoc99_scanf@plt>:
    12a0:	f3 0f 1e fa          	endbr64
    12a4:	ff 25 de 3c 00 00    	jmp    QWORD PTR [rip+0x3cde]        # 4f88 <__isoc99_scanf@GLIBC_2.7>
    12aa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000012b0 <fopen@plt>:
    12b0:	f3 0f 1e fa          	endbr64
    12b4:	ff 25 d6 3c 00 00    	jmp    QWORD PTR [rip+0x3cd6]        # 4f90 <fopen@GLIBC_2.2.5>
    12ba:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000012c0 <free@plt>:
    12c0:	f3 0f 1e fa          	endbr64
    12c4:	ff 25 ce 3c 00 00    	jmp    QWORD PTR [rip+0x3cce]        # 4f98 <free@GLIBC_2.2.5>
    12ca:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000012d0 <SHA256@plt>:
    12d0:	f3 0f 1e fa          	endbr64
    12d4:	ff 25 c6 3c 00 00    	jmp    QWORD PTR [rip+0x3cc6]        # 4fa0 <SHA256@OPENSSL_3.0.0>
    12da:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000012e0 <getchar@plt>:
    12e0:	f3 0f 1e fa          	endbr64
    12e4:	ff 25 be 3c 00 00    	jmp    QWORD PTR [rip+0x3cbe]        # 4fa8 <getchar@GLIBC_2.2.5>
    12ea:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000012f0 <strcmp@plt>:
    12f0:	f3 0f 1e fa          	endbr64
    12f4:	ff 25 b6 3c 00 00    	jmp    QWORD PTR [rip+0x3cb6]        # 4fb0 <strcmp@GLIBC_2.2.5>
    12fa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001300 <puts@plt>:
    1300:	f3 0f 1e fa          	endbr64
    1304:	ff 25 ae 3c 00 00    	jmp    QWORD PTR [rip+0x3cae]        # 4fb8 <puts@GLIBC_2.2.5>
    130a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001310 <strtok@plt>:
    1310:	f3 0f 1e fa          	endbr64
    1314:	ff 25 a6 3c 00 00    	jmp    QWORD PTR [rip+0x3ca6]        # 4fc0 <strtok@GLIBC_2.2.5>
    131a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001320 <fgets@plt>:
    1320:	f3 0f 1e fa          	endbr64
    1324:	ff 25 9e 3c 00 00    	jmp    QWORD PTR [rip+0x3c9e]        # 4fc8 <fgets@GLIBC_2.2.5>
    132a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001330 <strdup@plt>:
    1330:	f3 0f 1e fa          	endbr64
    1334:	ff 25 96 3c 00 00    	jmp    QWORD PTR [rip+0x3c96]        # 4fd0 <strdup@GLIBC_2.2.5>
    133a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .text:

0000000000001340 <_start>:
    1340:	f3 0f 1e fa          	endbr64
    1344:	31 ed                	xor    ebp,ebp
    1346:	49 89 d1             	mov    r9,rdx
    1349:	5e                   	pop    rsi
    134a:	48 89 e2             	mov    rdx,rsp
    134d:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
    1351:	50                   	push   rax
    1352:	54                   	push   rsp
    1353:	45 31 c0             	xor    r8d,r8d
    1356:	31 c9                	xor    ecx,ecx
    1358:	48 8d 3d db 0b 00 00 	lea    rdi,[rip+0xbdb]        # 1f3a <main>
    135f:	ff 15 7b 3c 00 00    	call   QWORD PTR [rip+0x3c7b]        # 4fe0 <__libc_start_main@GLIBC_2.34>
    1365:	f4                   	hlt
    1366:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    136d:	00 00 00 

0000000000001370 <deregister_tm_clones>:
    1370:	48 8d 3d 99 3c 00 00 	lea    rdi,[rip+0x3c99]        # 5010 <__TMC_END__>
    1377:	48 8d 05 92 3c 00 00 	lea    rax,[rip+0x3c92]        # 5010 <__TMC_END__>
    137e:	48 39 f8             	cmp    rax,rdi
    1381:	74 15                	je     1398 <deregister_tm_clones+0x28>
    1383:	48 8b 05 5e 3c 00 00 	mov    rax,QWORD PTR [rip+0x3c5e]        # 4fe8 <_ITM_deregisterTMCloneTable@Base>
    138a:	48 85 c0             	test   rax,rax
    138d:	74 09                	je     1398 <deregister_tm_clones+0x28>
    138f:	ff e0                	jmp    rax
    1391:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    1398:	c3                   	ret
    1399:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

00000000000013a0 <register_tm_clones>:
    13a0:	48 8d 3d 69 3c 00 00 	lea    rdi,[rip+0x3c69]        # 5010 <__TMC_END__>
    13a7:	48 8d 35 62 3c 00 00 	lea    rsi,[rip+0x3c62]        # 5010 <__TMC_END__>
    13ae:	48 29 fe             	sub    rsi,rdi
    13b1:	48 89 f0             	mov    rax,rsi
    13b4:	48 c1 ee 3f          	shr    rsi,0x3f
    13b8:	48 c1 f8 03          	sar    rax,0x3
    13bc:	48 01 c6             	add    rsi,rax
    13bf:	48 d1 fe             	sar    rsi,1
    13c2:	74 14                	je     13d8 <register_tm_clones+0x38>
    13c4:	48 8b 05 2d 3c 00 00 	mov    rax,QWORD PTR [rip+0x3c2d]        # 4ff8 <_ITM_registerTMCloneTable@Base>
    13cb:	48 85 c0             	test   rax,rax
    13ce:	74 08                	je     13d8 <register_tm_clones+0x38>
    13d0:	ff e0                	jmp    rax
    13d2:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    13d8:	c3                   	ret
    13d9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

00000000000013e0 <__do_global_dtors_aux>:
    13e0:	f3 0f 1e fa          	endbr64
    13e4:	80 3d 4d 3c 00 00 00 	cmp    BYTE PTR [rip+0x3c4d],0x0        # 5038 <completed.0>
    13eb:	75 2b                	jne    1418 <__do_global_dtors_aux+0x38>
    13ed:	55                   	push   rbp
    13ee:	48 83 3d e2 3b 00 00 	cmp    QWORD PTR [rip+0x3be2],0x0        # 4fd8 <__cxa_finalize@GLIBC_2.2.5>
    13f5:	00 
    13f6:	48 89 e5             	mov    rbp,rsp
    13f9:	74 0c                	je     1407 <__do_global_dtors_aux+0x27>
    13fb:	48 8b 3d 06 3c 00 00 	mov    rdi,QWORD PTR [rip+0x3c06]        # 5008 <__dso_handle>
    1402:	e8 a9 fd ff ff       	call   11b0 <__cxa_finalize@plt>
    1407:	e8 64 ff ff ff       	call   1370 <deregister_tm_clones>
    140c:	c6 05 25 3c 00 00 01 	mov    BYTE PTR [rip+0x3c25],0x1        # 5038 <completed.0>
    1413:	5d                   	pop    rbp
    1414:	c3                   	ret
    1415:	0f 1f 00             	nop    DWORD PTR [rax]
    1418:	c3                   	ret
    1419:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000001420 <frame_dummy>:
    1420:	f3 0f 1e fa          	endbr64
    1424:	e9 77 ff ff ff       	jmp    13a0 <register_tm_clones>

0000000000001429 <ecall_handler>:
    1429:	f3 0f 1e fa          	endbr64
    142d:	55                   	push   rbp
    142e:	48 89 e5             	mov    rbp,rsp
    1431:	48 81 ec b0 00 00 00 	sub    rsp,0xb0
    1438:	48 89 bd 58 ff ff ff 	mov    QWORD PTR [rbp-0xa8],rdi
    143f:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    1446:	00 00 
    1448:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
    144c:	31 c0                	xor    eax,eax
    144e:	48 8b 85 58 ff ff ff 	mov    rax,QWORD PTR [rbp-0xa8]
    1455:	8b 40 28             	mov    eax,DWORD PTR [rax+0x28]
    1458:	3d 39 05 00 00       	cmp    eax,0x539
    145d:	0f 85 85 00 00 00    	jne    14e8 <ecall_handler+0xbf>
    1463:	48 8d 05 9e 1b 00 00 	lea    rax,[rip+0x1b9e]        # 3008 <_IO_stdin_used+0x8>
    146a:	48 89 c7             	mov    rdi,rax
    146d:	e8 8e fe ff ff       	call   1300 <puts@plt>
    1472:	48 8d 05 b3 1b 00 00 	lea    rax,[rip+0x1bb3]        # 302c <_IO_stdin_used+0x2c>
    1479:	48 89 c6             	mov    rsi,rax
    147c:	48 8d 05 ab 1b 00 00 	lea    rax,[rip+0x1bab]        # 302e <_IO_stdin_used+0x2e>
    1483:	48 89 c7             	mov    rdi,rax
    1486:	e8 25 fe ff ff       	call   12b0 <fopen@plt>
    148b:	48 89 85 68 ff ff ff 	mov    QWORD PTR [rbp-0x98],rax
    1492:	48 83 bd 68 ff ff ff 	cmp    QWORD PTR [rbp-0x98],0x0
    1499:	00 
    149a:	74 3b                	je     14d7 <ecall_handler+0xae>
    149c:	48 8b 95 68 ff ff ff 	mov    rdx,QWORD PTR [rbp-0x98]
    14a3:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
    14aa:	be 80 00 00 00       	mov    esi,0x80
    14af:	48 89 c7             	mov    rdi,rax
    14b2:	e8 69 fe ff ff       	call   1320 <fgets@plt>
    14b7:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
    14be:	48 89 c7             	mov    rdi,rax
    14c1:	e8 3a fe ff ff       	call   1300 <puts@plt>
    14c6:	48 8b 85 68 ff ff ff 	mov    rax,QWORD PTR [rbp-0x98]
    14cd:	48 89 c7             	mov    rdi,rax
    14d0:	e8 ab fd ff ff       	call   1280 <fclose@plt>
    14d5:	eb 31                	jmp    1508 <ecall_handler+0xdf>
    14d7:	48 8d 05 5a 1b 00 00 	lea    rax,[rip+0x1b5a]        # 3038 <_IO_stdin_used+0x38>
    14de:	48 89 c7             	mov    rdi,rax
    14e1:	e8 1a fe ff ff       	call   1300 <puts@plt>
    14e6:	eb 20                	jmp    1508 <ecall_handler+0xdf>
    14e8:	48 8b 85 58 ff ff ff 	mov    rax,QWORD PTR [rbp-0xa8]
    14ef:	8b 40 28             	mov    eax,DWORD PTR [rax+0x28]
    14f2:	89 c6                	mov    esi,eax
    14f4:	48 8d 05 5c 1b 00 00 	lea    rax,[rip+0x1b5c]        # 3057 <_IO_stdin_used+0x57>
    14fb:	48 89 c7             	mov    rdi,rax
    14fe:	b8 00 00 00 00       	mov    eax,0x0
    1503:	e8 c8 fc ff ff       	call   11d0 <printf@plt>
    1508:	90                   	nop
    1509:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    150d:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    1514:	00 00 
    1516:	74 05                	je     151d <ecall_handler+0xf4>
    1518:	e8 73 fd ff ff       	call   1290 <__stack_chk_fail@plt>
    151d:	c9                   	leave
    151e:	c3                   	ret

000000000000151f <execute_rv_code>:
    151f:	f3 0f 1e fa          	endbr64
    1523:	55                   	push   rbp
    1524:	48 89 e5             	mov    rbp,rsp
    1527:	53                   	push   rbx
    1528:	48 81 ec 08 01 00 00 	sub    rsp,0x108
    152f:	48 89 bd f8 fe ff ff 	mov    QWORD PTR [rbp-0x108],rdi
    1536:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    153d:	00 00 
    153f:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
    1543:	31 c0                	xor    eax,eax
    1545:	48 8d 95 20 ff ff ff 	lea    rdx,[rbp-0xe0]
    154c:	b8 00 00 00 00       	mov    eax,0x0
    1551:	b9 18 00 00 00       	mov    ecx,0x18
    1556:	48 89 d7             	mov    rdi,rdx
    1559:	f3 48 ab             	rep stos QWORD PTR es:[rdi],rax
    155c:	48 89 fa             	mov    rdx,rdi
    155f:	89 02                	mov    DWORD PTR [rdx],eax
    1561:	48 83 c2 04          	add    rdx,0x4
    1565:	48 8b 85 f8 fe ff ff 	mov    rax,QWORD PTR [rbp-0x108]
    156c:	48 8b 08             	mov    rcx,QWORD PTR [rax]
    156f:	48 8b 58 08          	mov    rbx,QWORD PTR [rax+0x8]
    1573:	48 89 4d a4          	mov    QWORD PTR [rbp-0x5c],rcx
    1577:	48 89 5d ac          	mov    QWORD PTR [rbp-0x54],rbx
    157b:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
    157f:	48 8b 58 18          	mov    rbx,QWORD PTR [rax+0x18]
    1583:	48 89 4d b4          	mov    QWORD PTR [rbp-0x4c],rcx
    1587:	48 89 5d bc          	mov    QWORD PTR [rbp-0x44],rbx
    158b:	48 8b 48 20          	mov    rcx,QWORD PTR [rax+0x20]
    158f:	48 8b 58 28          	mov    rbx,QWORD PTR [rax+0x28]
    1593:	48 89 4d c4          	mov    QWORD PTR [rbp-0x3c],rcx
    1597:	48 89 5d cc          	mov    QWORD PTR [rbp-0x34],rbx
    159b:	48 8b 50 38          	mov    rdx,QWORD PTR [rax+0x38]
    159f:	48 8b 40 30          	mov    rax,QWORD PTR [rax+0x30]
    15a3:	48 89 45 d4          	mov    QWORD PTR [rbp-0x2c],rax
    15a7:	48 89 55 dc          	mov    QWORD PTR [rbp-0x24],rdx
    15ab:	48 8d 05 c6 1a 00 00 	lea    rax,[rip+0x1ac6]        # 3078 <_IO_stdin_used+0x78>
    15b2:	48 89 c7             	mov    rdi,rax
    15b5:	e8 46 fd ff ff       	call   1300 <puts@plt>
    15ba:	e9 0a 01 00 00       	jmp    16c9 <execute_rv_code+0x1aa>
    15bf:	8b 55 a0             	mov    edx,DWORD PTR [rbp-0x60]
    15c2:	48 8d 85 20 ff ff ff 	lea    rax,[rbp-0xe0]
    15c9:	89 d2                	mov    edx,edx
    15cb:	48 83 ea 80          	sub    rdx,0xffffffffffffff80
    15cf:	48 01 d0             	add    rax,rdx
    15d2:	48 83 c0 04          	add    rax,0x4
    15d6:	8b 00                	mov    eax,DWORD PTR [rax]
    15d8:	89 85 0c ff ff ff    	mov    DWORD PTR [rbp-0xf4],eax
    15de:	8b 85 0c ff ff ff    	mov    eax,DWORD PTR [rbp-0xf4]
    15e4:	83 e0 7f             	and    eax,0x7f
    15e7:	89 85 10 ff ff ff    	mov    DWORD PTR [rbp-0xf0],eax
    15ed:	83 bd 0c ff ff ff 00 	cmp    DWORD PTR [rbp-0xf4],0x0
    15f4:	0f 84 dd 00 00 00    	je     16d7 <execute_rv_code+0x1b8>
    15fa:	83 bd 10 ff ff ff 13 	cmp    DWORD PTR [rbp-0xf0],0x13
    1601:	74 0e                	je     1611 <execute_rv_code+0xf2>
    1603:	83 bd 10 ff ff ff 73 	cmp    DWORD PTR [rbp-0xf0],0x73
    160a:	74 65                	je     1671 <execute_rv_code+0x152>
    160c:	e9 8d 00 00 00       	jmp    169e <execute_rv_code+0x17f>
    1611:	8b 85 0c ff ff ff    	mov    eax,DWORD PTR [rbp-0xf4]
    1617:	c1 e8 07             	shr    eax,0x7
    161a:	83 e0 1f             	and    eax,0x1f
    161d:	89 85 14 ff ff ff    	mov    DWORD PTR [rbp-0xec],eax
    1623:	8b 85 0c ff ff ff    	mov    eax,DWORD PTR [rbp-0xf4]
    1629:	c1 e8 0f             	shr    eax,0xf
    162c:	83 e0 1f             	and    eax,0x1f
    162f:	89 85 18 ff ff ff    	mov    DWORD PTR [rbp-0xe8],eax
    1635:	8b 85 0c ff ff ff    	mov    eax,DWORD PTR [rbp-0xf4]
    163b:	c1 f8 14             	sar    eax,0x14
    163e:	89 85 1c ff ff ff    	mov    DWORD PTR [rbp-0xe4],eax
    1644:	83 bd 14 ff ff ff 00 	cmp    DWORD PTR [rbp-0xec],0x0
    164b:	74 6f                	je     16bc <execute_rv_code+0x19d>
    164d:	8b 85 18 ff ff ff    	mov    eax,DWORD PTR [rbp-0xe8]
    1653:	8b 94 85 20 ff ff ff 	mov    edx,DWORD PTR [rbp+rax*4-0xe0]
    165a:	8b 85 1c ff ff ff    	mov    eax,DWORD PTR [rbp-0xe4]
    1660:	01 c2                	add    edx,eax
    1662:	8b 85 14 ff ff ff    	mov    eax,DWORD PTR [rbp-0xec]
    1668:	89 94 85 20 ff ff ff 	mov    DWORD PTR [rbp+rax*4-0xe0],edx
    166f:	eb 4b                	jmp    16bc <execute_rv_code+0x19d>
    1671:	8b 85 0c ff ff ff    	mov    eax,DWORD PTR [rbp-0xf4]
    1677:	c1 e8 14             	shr    eax,0x14
    167a:	85 c0                	test   eax,eax
    167c:	75 41                	jne    16bf <execute_rv_code+0x1a0>
    167e:	48 8d 85 20 ff ff ff 	lea    rax,[rbp-0xe0]
    1685:	48 89 c7             	mov    rdi,rax
    1688:	e8 9c fd ff ff       	call   1429 <ecall_handler>
    168d:	48 8d 05 05 1a 00 00 	lea    rax,[rip+0x1a05]        # 3099 <_IO_stdin_used+0x99>
    1694:	48 89 c7             	mov    rdi,rax
    1697:	e8 64 fc ff ff       	call   1300 <puts@plt>
    169c:	eb 49                	jmp    16e7 <execute_rv_code+0x1c8>
    169e:	8b 85 10 ff ff ff    	mov    eax,DWORD PTR [rbp-0xf0]
    16a4:	89 c6                	mov    esi,eax
    16a6:	48 8d 05 04 1a 00 00 	lea    rax,[rip+0x1a04]        # 30b1 <_IO_stdin_used+0xb1>
    16ad:	48 89 c7             	mov    rdi,rax
    16b0:	b8 00 00 00 00       	mov    eax,0x0
    16b5:	e8 16 fb ff ff       	call   11d0 <printf@plt>
    16ba:	eb 2b                	jmp    16e7 <execute_rv_code+0x1c8>
    16bc:	90                   	nop
    16bd:	eb 01                	jmp    16c0 <execute_rv_code+0x1a1>
    16bf:	90                   	nop
    16c0:	8b 45 a0             	mov    eax,DWORD PTR [rbp-0x60]
    16c3:	83 c0 04             	add    eax,0x4
    16c6:	89 45 a0             	mov    DWORD PTR [rbp-0x60],eax
    16c9:	8b 45 a0             	mov    eax,DWORD PTR [rbp-0x60]
    16cc:	83 f8 3f             	cmp    eax,0x3f
    16cf:	0f 86 ea fe ff ff    	jbe    15bf <execute_rv_code+0xa0>
    16d5:	eb 01                	jmp    16d8 <execute_rv_code+0x1b9>
    16d7:	90                   	nop
    16d8:	48 8d 05 ba 19 00 00 	lea    rax,[rip+0x19ba]        # 3099 <_IO_stdin_used+0x99>
    16df:	48 89 c7             	mov    rdi,rax
    16e2:	e8 19 fc ff ff       	call   1300 <puts@plt>
    16e7:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    16eb:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    16f2:	00 00 
    16f4:	74 05                	je     16fb <execute_rv_code+0x1dc>
    16f6:	e8 95 fb ff ff       	call   1290 <__stack_chk_fail@plt>
    16fb:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
    16ff:	c9                   	leave
    1700:	c3                   	ret

0000000000001701 <get_reg_num>:
    1701:	f3 0f 1e fa          	endbr64
    1705:	55                   	push   rbp
    1706:	48 89 e5             	mov    rbp,rsp
    1709:	48 83 ec 20          	sub    rsp,0x20
    170d:	48 89 7d e8          	mov    QWORD PTR [rbp-0x18],rdi
    1711:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    1715:	be 2c 00 00 00       	mov    esi,0x2c
    171a:	48 89 c7             	mov    rdi,rax
    171d:	e8 ce fa ff ff       	call   11f0 <strchr@plt>
    1722:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
    1726:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
    172b:	74 07                	je     1734 <get_reg_num+0x33>
    172d:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1731:	c6 00 00             	mov    BYTE PTR [rax],0x0
    1734:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    1738:	48 8d 15 8c 19 00 00 	lea    rdx,[rip+0x198c]        # 30cb <_IO_stdin_used+0xcb>
    173f:	48 89 d6             	mov    rsi,rdx
    1742:	48 89 c7             	mov    rdi,rax
    1745:	e8 a6 fb ff ff       	call   12f0 <strcmp@plt>
    174a:	85 c0                	test   eax,eax
    174c:	74 1a                	je     1768 <get_reg_num+0x67>
    174e:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    1752:	48 8d 15 77 19 00 00 	lea    rdx,[rip+0x1977]        # 30d0 <_IO_stdin_used+0xd0>
    1759:	48 89 d6             	mov    rsi,rdx
    175c:	48 89 c7             	mov    rdi,rax
    175f:	e8 8c fb ff ff       	call   12f0 <strcmp@plt>
    1764:	85 c0                	test   eax,eax
    1766:	75 0a                	jne    1772 <get_reg_num+0x71>
    1768:	b8 00 00 00 00       	mov    eax,0x0
    176d:	e9 f4 00 00 00       	jmp    1866 <get_reg_num+0x165>
    1772:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    1776:	48 8d 15 56 19 00 00 	lea    rdx,[rip+0x1956]        # 30d3 <_IO_stdin_used+0xd3>
    177d:	48 89 d6             	mov    rsi,rdx
    1780:	48 89 c7             	mov    rdi,rax
    1783:	e8 68 fb ff ff       	call   12f0 <strcmp@plt>
    1788:	85 c0                	test   eax,eax
    178a:	74 1a                	je     17a6 <get_reg_num+0xa5>
    178c:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    1790:	48 8d 15 3f 19 00 00 	lea    rdx,[rip+0x193f]        # 30d6 <_IO_stdin_used+0xd6>
    1797:	48 89 d6             	mov    rsi,rdx
    179a:	48 89 c7             	mov    rdi,rax
    179d:	e8 4e fb ff ff       	call   12f0 <strcmp@plt>
    17a2:	85 c0                	test   eax,eax
    17a4:	75 0a                	jne    17b0 <get_reg_num+0xaf>
    17a6:	b8 01 00 00 00       	mov    eax,0x1
    17ab:	e9 b6 00 00 00       	jmp    1866 <get_reg_num+0x165>
    17b0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    17b4:	48 8d 15 1e 19 00 00 	lea    rdx,[rip+0x191e]        # 30d9 <_IO_stdin_used+0xd9>
    17bb:	48 89 d6             	mov    rsi,rdx
    17be:	48 89 c7             	mov    rdi,rax
    17c1:	e8 2a fb ff ff       	call   12f0 <strcmp@plt>
    17c6:	85 c0                	test   eax,eax
    17c8:	74 1a                	je     17e4 <get_reg_num+0xe3>
    17ca:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    17ce:	48 8d 15 07 19 00 00 	lea    rdx,[rip+0x1907]        # 30dc <_IO_stdin_used+0xdc>
    17d5:	48 89 d6             	mov    rsi,rdx
    17d8:	48 89 c7             	mov    rdi,rax
    17db:	e8 10 fb ff ff       	call   12f0 <strcmp@plt>
    17e0:	85 c0                	test   eax,eax
    17e2:	75 07                	jne    17eb <get_reg_num+0xea>
    17e4:	b8 02 00 00 00       	mov    eax,0x2
    17e9:	eb 7b                	jmp    1866 <get_reg_num+0x165>
    17eb:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    17ef:	48 8d 15 e9 18 00 00 	lea    rdx,[rip+0x18e9]        # 30df <_IO_stdin_used+0xdf>
    17f6:	48 89 d6             	mov    rsi,rdx
    17f9:	48 89 c7             	mov    rdi,rax
    17fc:	e8 ef fa ff ff       	call   12f0 <strcmp@plt>
    1801:	85 c0                	test   eax,eax
    1803:	74 1a                	je     181f <get_reg_num+0x11e>
    1805:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    1809:	48 8d 15 d2 18 00 00 	lea    rdx,[rip+0x18d2]        # 30e2 <_IO_stdin_used+0xe2>
    1810:	48 89 d6             	mov    rsi,rdx
    1813:	48 89 c7             	mov    rdi,rax
    1816:	e8 d5 fa ff ff       	call   12f0 <strcmp@plt>
    181b:	85 c0                	test   eax,eax
    181d:	75 07                	jne    1826 <get_reg_num+0x125>
    181f:	b8 0a 00 00 00       	mov    eax,0xa
    1824:	eb 40                	jmp    1866 <get_reg_num+0x165>
    1826:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    182a:	48 8d 15 b5 18 00 00 	lea    rdx,[rip+0x18b5]        # 30e6 <_IO_stdin_used+0xe6>
    1831:	48 89 d6             	mov    rsi,rdx
    1834:	48 89 c7             	mov    rdi,rax
    1837:	e8 b4 fa ff ff       	call   12f0 <strcmp@plt>
    183c:	85 c0                	test   eax,eax
    183e:	74 1a                	je     185a <get_reg_num+0x159>
    1840:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    1844:	48 8d 15 9e 18 00 00 	lea    rdx,[rip+0x189e]        # 30e9 <_IO_stdin_used+0xe9>
    184b:	48 89 d6             	mov    rsi,rdx
    184e:	48 89 c7             	mov    rdi,rax
    1851:	e8 9a fa ff ff       	call   12f0 <strcmp@plt>
    1856:	85 c0                	test   eax,eax
    1858:	75 07                	jne    1861 <get_reg_num+0x160>
    185a:	b8 0b 00 00 00       	mov    eax,0xb
    185f:	eb 05                	jmp    1866 <get_reg_num+0x165>
    1861:	b8 ff ff ff ff       	mov    eax,0xffffffff
    1866:	c9                   	leave
    1867:	c3                   	ret

0000000000001868 <assemble_rv_code>:
    1868:	f3 0f 1e fa          	endbr64
    186c:	55                   	push   rbp
    186d:	48 89 e5             	mov    rbp,rsp
    1870:	48 83 ec 60          	sub    rsp,0x60
    1874:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
    1878:	48 89 75 a0          	mov    QWORD PTR [rbp-0x60],rsi
    187c:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    1883:	00 00 
    1885:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
    1889:	31 c0                	xor    eax,eax
    188b:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
    188f:	48 89 c7             	mov    rdi,rax
    1892:	e8 99 fa ff ff       	call   1330 <strdup@plt>
    1897:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
    189b:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
    189f:	48 8d 15 47 18 00 00 	lea    rdx,[rip+0x1847]        # 30ed <_IO_stdin_used+0xed>
    18a6:	48 89 d6             	mov    rsi,rdx
    18a9:	48 89 c7             	mov    rdi,rax
    18ac:	e8 5f fa ff ff       	call   1310 <strtok@plt>
    18b1:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
    18b5:	c7 45 bc 00 00 00 00 	mov    DWORD PTR [rbp-0x44],0x0
    18bc:	e9 cd 01 00 00       	jmp    1a8e <assemble_rv_code+0x226>
    18c1:	83 7d bc 3f          	cmp    DWORD PTR [rbp-0x44],0x3f
    18c5:	7e 25                	jle    18ec <assemble_rv_code+0x84>
    18c7:	48 8d 05 22 18 00 00 	lea    rax,[rip+0x1822]        # 30f0 <_IO_stdin_used+0xf0>
    18ce:	48 89 c7             	mov    rdi,rax
    18d1:	e8 2a fa ff ff       	call   1300 <puts@plt>
    18d6:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
    18da:	48 89 c7             	mov    rdi,rax
    18dd:	e8 de f9 ff ff       	call   12c0 <free@plt>
    18e2:	b8 ff ff ff ff       	mov    eax,0xffffffff
    18e7:	e9 bc 01 00 00       	jmp    1aa8 <assemble_rv_code+0x240>
    18ec:	48 c7 45 da 00 00 00 	mov    QWORD PTR [rbp-0x26],0x0
    18f3:	00 
    18f4:	66 c7 45 e2 00 00    	mov    WORD PTR [rbp-0x1e],0x0
    18fa:	48 8d 55 da          	lea    rdx,[rbp-0x26]
    18fe:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
    1902:	48 8d 0d 07 18 00 00 	lea    rcx,[rip+0x1807]        # 3110 <_IO_stdin_used+0x110>
    1909:	48 89 ce             	mov    rsi,rcx
    190c:	48 89 c7             	mov    rdi,rax
    190f:	b8 00 00 00 00       	mov    eax,0x0
    1914:	e8 57 f9 ff ff       	call   1270 <__isoc99_sscanf@plt>
    1919:	c7 45 b4 00 00 00 00 	mov    DWORD PTR [rbp-0x4c],0x0
    1920:	48 8d 45 da          	lea    rax,[rbp-0x26]
    1924:	48 8d 15 e9 17 00 00 	lea    rdx,[rip+0x17e9]        # 3114 <_IO_stdin_used+0x114>
    192b:	48 89 d6             	mov    rsi,rdx
    192e:	48 89 c7             	mov    rdi,rax
    1931:	e8 ba f9 ff ff       	call   12f0 <strcmp@plt>
    1936:	85 c0                	test   eax,eax
    1938:	0f 85 bf 00 00 00    	jne    19fd <assemble_rv_code+0x195>
    193e:	48 8d 75 b8          	lea    rsi,[rbp-0x48]
    1942:	48 8d 4d ee          	lea    rcx,[rbp-0x12]
    1946:	48 8d 55 e4          	lea    rdx,[rbp-0x1c]
    194a:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
    194e:	49 89 f0             	mov    r8,rsi
    1951:	48 8d 35 c1 17 00 00 	lea    rsi,[rip+0x17c1]        # 3119 <_IO_stdin_used+0x119>
    1958:	48 89 c7             	mov    rdi,rax
    195b:	b8 00 00 00 00       	mov    eax,0x0
    1960:	e8 0b f9 ff ff       	call   1270 <__isoc99_sscanf@plt>
    1965:	83 f8 03             	cmp    eax,0x3
    1968:	74 22                	je     198c <assemble_rv_code+0x124>
    196a:	48 8d 05 b7 17 00 00 	lea    rax,[rip+0x17b7]        # 3128 <_IO_stdin_used+0x128>
    1971:	48 89 c7             	mov    rdi,rax
    1974:	e8 87 f9 ff ff       	call   1300 <puts@plt>
    1979:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
    197d:	48 89 c7             	mov    rdi,rax
    1980:	e8 3b f9 ff ff       	call   12c0 <free@plt>
    1985:	b8 ff ff ff ff       	mov    eax,0xffffffff
    198a:	eb 6c                	jmp    19f8 <assemble_rv_code+0x190>
    198c:	48 8d 45 e4          	lea    rax,[rbp-0x1c]
    1990:	48 89 c7             	mov    rdi,rax
    1993:	e8 69 fd ff ff       	call   1701 <get_reg_num>
    1998:	89 45 c0             	mov    DWORD PTR [rbp-0x40],eax
    199b:	48 8d 45 ee          	lea    rax,[rbp-0x12]
    199f:	48 89 c7             	mov    rdi,rax
    19a2:	e8 5a fd ff ff       	call   1701 <get_reg_num>
    19a7:	89 45 c4             	mov    DWORD PTR [rbp-0x3c],eax
    19aa:	83 7d c0 ff          	cmp    DWORD PTR [rbp-0x40],0xffffffff
    19ae:	74 06                	je     19b6 <assemble_rv_code+0x14e>
    19b0:	83 7d c4 ff          	cmp    DWORD PTR [rbp-0x3c],0xffffffff
    19b4:	75 22                	jne    19d8 <assemble_rv_code+0x170>
    19b6:	48 8d 05 8b 17 00 00 	lea    rax,[rip+0x178b]        # 3148 <_IO_stdin_used+0x148>
    19bd:	48 89 c7             	mov    rdi,rax
    19c0:	e8 3b f9 ff ff       	call   1300 <puts@plt>
    19c5:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
    19c9:	48 89 c7             	mov    rdi,rax
    19cc:	e8 ef f8 ff ff       	call   12c0 <free@plt>
    19d1:	b8 ff ff ff ff       	mov    eax,0xffffffff
    19d6:	eb 20                	jmp    19f8 <assemble_rv_code+0x190>
    19d8:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
    19db:	c1 e0 14             	shl    eax,0x14
    19de:	89 c2                	mov    edx,eax
    19e0:	8b 45 c4             	mov    eax,DWORD PTR [rbp-0x3c]
    19e3:	c1 e0 0f             	shl    eax,0xf
    19e6:	09 c2                	or     edx,eax
    19e8:	8b 45 c0             	mov    eax,DWORD PTR [rbp-0x40]
    19eb:	c1 e0 07             	shl    eax,0x7
    19ee:	09 d0                	or     eax,edx
    19f0:	83 c8 13             	or     eax,0x13
    19f3:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
    19f6:	eb 61                	jmp    1a59 <assemble_rv_code+0x1f1>
    19f8:	e9 ab 00 00 00       	jmp    1aa8 <assemble_rv_code+0x240>
    19fd:	48 8d 45 da          	lea    rax,[rbp-0x26]
    1a01:	48 8d 15 63 17 00 00 	lea    rdx,[rip+0x1763]        # 316b <_IO_stdin_used+0x16b>
    1a08:	48 89 d6             	mov    rsi,rdx
    1a0b:	48 89 c7             	mov    rdi,rax
    1a0e:	e8 dd f8 ff ff       	call   12f0 <strcmp@plt>
    1a13:	85 c0                	test   eax,eax
    1a15:	75 09                	jne    1a20 <assemble_rv_code+0x1b8>
    1a17:	c7 45 b4 73 00 00 00 	mov    DWORD PTR [rbp-0x4c],0x73
    1a1e:	eb 39                	jmp    1a59 <assemble_rv_code+0x1f1>
    1a20:	48 8d 45 da          	lea    rax,[rbp-0x26]
    1a24:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    1a27:	84 c0                	test   al,al
    1a29:	74 2e                	je     1a59 <assemble_rv_code+0x1f1>
    1a2b:	48 8d 45 da          	lea    rax,[rbp-0x26]
    1a2f:	48 89 c6             	mov    rsi,rax
    1a32:	48 8d 05 38 17 00 00 	lea    rax,[rip+0x1738]        # 3171 <_IO_stdin_used+0x171>
    1a39:	48 89 c7             	mov    rdi,rax
    1a3c:	b8 00 00 00 00       	mov    eax,0x0
    1a41:	e8 8a f7 ff ff       	call   11d0 <printf@plt>
    1a46:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
    1a4a:	48 89 c7             	mov    rdi,rax
    1a4d:	e8 6e f8 ff ff       	call   12c0 <free@plt>
    1a52:	b8 ff ff ff ff       	mov    eax,0xffffffff
    1a57:	eb 4f                	jmp    1aa8 <assemble_rv_code+0x240>
    1a59:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
    1a5c:	85 c0                	test   eax,eax
    1a5e:	74 16                	je     1a76 <assemble_rv_code+0x20e>
    1a60:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
    1a63:	48 63 d0             	movsxd rdx,eax
    1a66:	48 8b 45 a0          	mov    rax,QWORD PTR [rbp-0x60]
    1a6a:	48 01 c2             	add    rdx,rax
    1a6d:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
    1a70:	89 02                	mov    DWORD PTR [rdx],eax
    1a72:	83 45 bc 04          	add    DWORD PTR [rbp-0x44],0x4
    1a76:	48 8d 05 70 16 00 00 	lea    rax,[rip+0x1670]        # 30ed <_IO_stdin_used+0xed>
    1a7d:	48 89 c6             	mov    rsi,rax
    1a80:	bf 00 00 00 00       	mov    edi,0x0
    1a85:	e8 86 f8 ff ff       	call   1310 <strtok@plt>
    1a8a:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
    1a8e:	48 83 7d c8 00       	cmp    QWORD PTR [rbp-0x38],0x0
    1a93:	0f 85 28 fe ff ff    	jne    18c1 <assemble_rv_code+0x59>
    1a99:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
    1a9d:	48 89 c7             	mov    rdi,rax
    1aa0:	e8 1b f8 ff ff       	call   12c0 <free@plt>
    1aa5:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
    1aa8:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
    1aac:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    1ab3:	00 00 
    1ab5:	74 05                	je     1abc <assemble_rv_code+0x254>
    1ab7:	e8 d4 f7 ff ff       	call   1290 <__stack_chk_fail@plt>
    1abc:	c9                   	leave
    1abd:	c3                   	ret

0000000000001abe <calculate_hash>:
    1abe:	f3 0f 1e fa          	endbr64
    1ac2:	55                   	push   rbp
    1ac3:	48 89 e5             	mov    rbp,rsp
    1ac6:	48 81 ec 50 02 00 00 	sub    rsp,0x250
    1acd:	48 89 bd b8 fd ff ff 	mov    QWORD PTR [rbp-0x248],rdi
    1ad4:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    1adb:	00 00 
    1add:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
    1ae1:	31 c0                	xor    eax,eax
    1ae3:	48 8b 85 b8 fd ff ff 	mov    rax,QWORD PTR [rbp-0x248]
    1aea:	8b b0 d4 00 00 00    	mov    esi,DWORD PTR [rax+0xd4]
    1af0:	48 8b 85 b8 fd ff ff 	mov    rax,QWORD PTR [rbp-0x248]
    1af7:	48 8d 78 50          	lea    rdi,[rax+0x50]
    1afb:	48 8b 85 b8 fd ff ff 	mov    rax,QWORD PTR [rbp-0x248]
    1b02:	48 8b 48 08          	mov    rcx,QWORD PTR [rax+0x8]
    1b06:	48 8b 85 b8 fd ff ff 	mov    rax,QWORD PTR [rbp-0x248]
    1b0d:	8b 10                	mov    edx,DWORD PTR [rax]
    1b0f:	48 8d 85 f0 fd ff ff 	lea    rax,[rbp-0x210]
    1b16:	41 89 f1             	mov    r9d,esi
    1b19:	49 89 f8             	mov    r8,rdi
    1b1c:	48 8d 35 6b 16 00 00 	lea    rsi,[rip+0x166b]        # 318e <_IO_stdin_used+0x18e>
    1b23:	48 89 c7             	mov    rdi,rax
    1b26:	b8 00 00 00 00       	mov    eax,0x0
    1b2b:	e8 b0 f6 ff ff       	call   11e0 <sprintf@plt>
    1b30:	89 85 cc fd ff ff    	mov    DWORD PTR [rbp-0x234],eax
    1b36:	48 8b 85 b8 fd ff ff 	mov    rax,QWORD PTR [rbp-0x248]
    1b3d:	48 8d 48 10          	lea    rcx,[rax+0x10]
    1b41:	8b 85 cc fd ff ff    	mov    eax,DWORD PTR [rbp-0x234]
    1b47:	48 98                	cdqe
    1b49:	48 8d 95 f0 fd ff ff 	lea    rdx,[rbp-0x210]
    1b50:	48 01 d0             	add    rax,rdx
    1b53:	ba 40 00 00 00       	mov    edx,0x40
    1b58:	48 89 ce             	mov    rsi,rcx
    1b5b:	48 89 c7             	mov    rdi,rax
    1b5e:	e8 dd f6 ff ff       	call   1240 <memcpy@plt>
    1b63:	8b 85 cc fd ff ff    	mov    eax,DWORD PTR [rbp-0x234]
    1b69:	83 c0 40             	add    eax,0x40
    1b6c:	48 63 c8             	movsxd rcx,eax
    1b6f:	48 8d 95 d0 fd ff ff 	lea    rdx,[rbp-0x230]
    1b76:	48 8d 85 f0 fd ff ff 	lea    rax,[rbp-0x210]
    1b7d:	48 89 ce             	mov    rsi,rcx
    1b80:	48 89 c7             	mov    rdi,rax
    1b83:	e8 48 f7 ff ff       	call   12d0 <SHA256@plt>
    1b88:	c7 85 c8 fd ff ff 00 	mov    DWORD PTR [rbp-0x238],0x0
    1b8f:	00 00 00 
    1b92:	eb 4f                	jmp    1be3 <calculate_hash+0x125>
    1b94:	8b 85 c8 fd ff ff    	mov    eax,DWORD PTR [rbp-0x238]
    1b9a:	48 98                	cdqe
    1b9c:	0f b6 84 05 d0 fd ff 	movzx  eax,BYTE PTR [rbp+rax*1-0x230]
    1ba3:	ff 
    1ba4:	0f b6 c0             	movzx  eax,al
    1ba7:	48 8b 95 b8 fd ff ff 	mov    rdx,QWORD PTR [rbp-0x248]
    1bae:	48 8d 8a 91 00 00 00 	lea    rcx,[rdx+0x91]
    1bb5:	8b 95 c8 fd ff ff    	mov    edx,DWORD PTR [rbp-0x238]
    1bbb:	01 d2                	add    edx,edx
    1bbd:	48 63 d2             	movsxd rdx,edx
    1bc0:	48 01 d1             	add    rcx,rdx
    1bc3:	89 c2                	mov    edx,eax
    1bc5:	48 8d 05 cc 15 00 00 	lea    rax,[rip+0x15cc]        # 3198 <_IO_stdin_used+0x198>
    1bcc:	48 89 c6             	mov    rsi,rax
    1bcf:	48 89 cf             	mov    rdi,rcx
    1bd2:	b8 00 00 00 00       	mov    eax,0x0
    1bd7:	e8 04 f6 ff ff       	call   11e0 <sprintf@plt>
    1bdc:	83 85 c8 fd ff ff 01 	add    DWORD PTR [rbp-0x238],0x1
    1be3:	83 bd c8 fd ff ff 1f 	cmp    DWORD PTR [rbp-0x238],0x1f
    1bea:	7e a8                	jle    1b94 <calculate_hash+0xd6>
    1bec:	48 8b 85 b8 fd ff ff 	mov    rax,QWORD PTR [rbp-0x248]
    1bf3:	c6 80 d1 00 00 00 00 	mov    BYTE PTR [rax+0xd1],0x0
    1bfa:	90                   	nop
    1bfb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1bff:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    1c06:	00 00 
    1c08:	74 05                	je     1c0f <calculate_hash+0x151>
    1c0a:	e8 81 f6 ff ff       	call   1290 <__stack_chk_fail@plt>
    1c0f:	c9                   	leave
    1c10:	c3                   	ret

0000000000001c11 <is_pow_valid>:
    1c11:	f3 0f 1e fa          	endbr64
    1c15:	55                   	push   rbp
    1c16:	48 89 e5             	mov    rbp,rsp
    1c19:	48 83 ec 10          	sub    rsp,0x10
    1c1d:	48 89 7d f8          	mov    QWORD PTR [rbp-0x8],rdi
    1c21:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1c25:	ba 03 00 00 00       	mov    edx,0x3
    1c2a:	48 8d 0d 6c 15 00 00 	lea    rcx,[rip+0x156c]        # 319d <_IO_stdin_used+0x19d>
    1c31:	48 89 ce             	mov    rsi,rcx
    1c34:	48 89 c7             	mov    rdi,rax
    1c37:	e8 d4 f5 ff ff       	call   1210 <strncmp@plt>
    1c3c:	85 c0                	test   eax,eax
    1c3e:	0f 94 c0             	sete   al
    1c41:	0f b6 c0             	movzx  eax,al
    1c44:	c9                   	leave
    1c45:	c3                   	ret

0000000000001c46 <is_block_valid>:
    1c46:	f3 0f 1e fa          	endbr64
    1c4a:	55                   	push   rbp
    1c4b:	48 89 e5             	mov    rbp,rsp
    1c4e:	48 83 ec 60          	sub    rsp,0x60
    1c52:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
    1c56:	48 89 75 a0          	mov    QWORD PTR [rbp-0x60],rsi
    1c5a:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    1c61:	00 00 
    1c63:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
    1c67:	31 c0                	xor    eax,eax
    1c69:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
    1c6d:	8b 80 d4 00 00 00    	mov    eax,DWORD PTR [rax+0xd4]
    1c73:	3d ef be ad de       	cmp    eax,0xdeadbeef
    1c78:	75 0a                	jne    1c84 <is_block_valid+0x3e>
    1c7a:	b8 01 00 00 00       	mov    eax,0x1
    1c7f:	e9 b3 00 00 00       	jmp    1d37 <is_block_valid+0xf1>
    1c84:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
    1c88:	8b 10                	mov    edx,DWORD PTR [rax]
    1c8a:	48 8b 45 a0          	mov    rax,QWORD PTR [rbp-0x60]
    1c8e:	8b 00                	mov    eax,DWORD PTR [rax]
    1c90:	83 c0 01             	add    eax,0x1
    1c93:	39 c2                	cmp    edx,eax
    1c95:	74 0a                	je     1ca1 <is_block_valid+0x5b>
    1c97:	b8 00 00 00 00       	mov    eax,0x0
    1c9c:	e9 96 00 00 00       	jmp    1d37 <is_block_valid+0xf1>
    1ca1:	48 8b 45 a0          	mov    rax,QWORD PTR [rbp-0x60]
    1ca5:	48 8d 90 91 00 00 00 	lea    rdx,[rax+0x91]
    1cac:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
    1cb0:	48 83 c0 50          	add    rax,0x50
    1cb4:	48 89 d6             	mov    rsi,rdx
    1cb7:	48 89 c7             	mov    rdi,rax
    1cba:	e8 31 f6 ff ff       	call   12f0 <strcmp@plt>
    1cbf:	85 c0                	test   eax,eax
    1cc1:	74 07                	je     1cca <is_block_valid+0x84>
    1cc3:	b8 00 00 00 00       	mov    eax,0x0
    1cc8:	eb 6d                	jmp    1d37 <is_block_valid+0xf1>
    1cca:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
    1cce:	48 8d 90 91 00 00 00 	lea    rdx,[rax+0x91]
    1cd5:	48 8d 45 b0          	lea    rax,[rbp-0x50]
    1cd9:	48 89 d6             	mov    rsi,rdx
    1cdc:	48 89 c7             	mov    rdi,rax
    1cdf:	e8 7c f5 ff ff       	call   1260 <strcpy@plt>
    1ce4:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
    1ce8:	48 89 c7             	mov    rdi,rax
    1ceb:	e8 ce fd ff ff       	call   1abe <calculate_hash>
    1cf0:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
    1cf4:	48 8d 90 91 00 00 00 	lea    rdx,[rax+0x91]
    1cfb:	48 8d 45 b0          	lea    rax,[rbp-0x50]
    1cff:	48 89 c6             	mov    rsi,rax
    1d02:	48 89 d7             	mov    rdi,rdx
    1d05:	e8 e6 f5 ff ff       	call   12f0 <strcmp@plt>
    1d0a:	85 c0                	test   eax,eax
    1d0c:	74 07                	je     1d15 <is_block_valid+0xcf>
    1d0e:	b8 00 00 00 00       	mov    eax,0x0
    1d13:	eb 22                	jmp    1d37 <is_block_valid+0xf1>
    1d15:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
    1d19:	48 05 91 00 00 00    	add    rax,0x91
    1d1f:	48 89 c7             	mov    rdi,rax
    1d22:	e8 ea fe ff ff       	call   1c11 <is_pow_valid>
    1d27:	85 c0                	test   eax,eax
    1d29:	75 07                	jne    1d32 <is_block_valid+0xec>
    1d2b:	b8 00 00 00 00       	mov    eax,0x0
    1d30:	eb 05                	jmp    1d37 <is_block_valid+0xf1>
    1d32:	b8 01 00 00 00       	mov    eax,0x1
    1d37:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
    1d3b:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    1d42:	00 00 
    1d44:	74 05                	je     1d4b <is_block_valid+0x105>
    1d46:	e8 45 f5 ff ff       	call   1290 <__stack_chk_fail@plt>
    1d4b:	c9                   	leave
    1d4c:	c3                   	ret

0000000000001d4d <add_block>:
    1d4d:	f3 0f 1e fa          	endbr64
    1d51:	55                   	push   rbp
    1d52:	48 89 e5             	mov    rbp,rsp
    1d55:	48 89 7d f8          	mov    QWORD PTR [rbp-0x8],rdi
    1d59:	8b 05 51 3b 00 00    	mov    eax,DWORD PTR [rip+0x3b51]        # 58b0 <chain_len>
    1d5f:	83 f8 09             	cmp    eax,0x9
    1d62:	0f 8f 6b 01 00 00    	jg     1ed3 <add_block+0x186>
    1d68:	8b 05 42 3b 00 00    	mov    eax,DWORD PTR [rip+0x3b42]        # 58b0 <chain_len>
    1d6e:	8d 50 01             	lea    edx,[rax+0x1]
    1d71:	89 15 39 3b 00 00    	mov    DWORD PTR [rip+0x3b39],edx        # 58b0 <chain_len>
    1d77:	48 63 d0             	movsxd rdx,eax
    1d7a:	48 89 d0             	mov    rax,rdx
    1d7d:	48 01 c0             	add    rax,rax
    1d80:	48 01 d0             	add    rax,rdx
    1d83:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
    1d8a:	00 
    1d8b:	48 01 d0             	add    rax,rdx
    1d8e:	48 c1 e0 03          	shl    rax,0x3
    1d92:	48 89 c1             	mov    rcx,rax
    1d95:	48 8d 15 a4 32 00 00 	lea    rdx,[rip+0x32a4]        # 5040 <blockchain>
    1d9c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1da0:	48 8b 30             	mov    rsi,QWORD PTR [rax]
    1da3:	48 8b 78 08          	mov    rdi,QWORD PTR [rax+0x8]
    1da7:	48 89 34 11          	mov    QWORD PTR [rcx+rdx*1],rsi
    1dab:	48 89 7c 11 08       	mov    QWORD PTR [rcx+rdx*1+0x8],rdi
    1db0:	48 8b 70 10          	mov    rsi,QWORD PTR [rax+0x10]
    1db4:	48 8b 78 18          	mov    rdi,QWORD PTR [rax+0x18]
    1db8:	48 89 74 11 10       	mov    QWORD PTR [rcx+rdx*1+0x10],rsi
    1dbd:	48 89 7c 11 18       	mov    QWORD PTR [rcx+rdx*1+0x18],rdi
    1dc2:	48 8b 70 20          	mov    rsi,QWORD PTR [rax+0x20]
    1dc6:	48 8b 78 28          	mov    rdi,QWORD PTR [rax+0x28]
    1dca:	48 89 74 11 20       	mov    QWORD PTR [rcx+rdx*1+0x20],rsi
    1dcf:	48 89 7c 11 28       	mov    QWORD PTR [rcx+rdx*1+0x28],rdi
    1dd4:	48 8b 70 30          	mov    rsi,QWORD PTR [rax+0x30]
    1dd8:	48 8b 78 38          	mov    rdi,QWORD PTR [rax+0x38]
    1ddc:	48 89 74 11 30       	mov    QWORD PTR [rcx+rdx*1+0x30],rsi
    1de1:	48 89 7c 11 38       	mov    QWORD PTR [rcx+rdx*1+0x38],rdi
    1de6:	48 8b 70 40          	mov    rsi,QWORD PTR [rax+0x40]
    1dea:	48 8b 78 48          	mov    rdi,QWORD PTR [rax+0x48]
    1dee:	48 89 74 11 40       	mov    QWORD PTR [rcx+rdx*1+0x40],rsi
    1df3:	48 89 7c 11 48       	mov    QWORD PTR [rcx+rdx*1+0x48],rdi
    1df8:	48 8b 70 50          	mov    rsi,QWORD PTR [rax+0x50]
    1dfc:	48 8b 78 58          	mov    rdi,QWORD PTR [rax+0x58]
    1e00:	48 89 74 11 50       	mov    QWORD PTR [rcx+rdx*1+0x50],rsi
    1e05:	48 89 7c 11 58       	mov    QWORD PTR [rcx+rdx*1+0x58],rdi
    1e0a:	48 8b 70 60          	mov    rsi,QWORD PTR [rax+0x60]
    1e0e:	48 8b 78 68          	mov    rdi,QWORD PTR [rax+0x68]
    1e12:	48 89 74 11 60       	mov    QWORD PTR [rcx+rdx*1+0x60],rsi
    1e17:	48 89 7c 11 68       	mov    QWORD PTR [rcx+rdx*1+0x68],rdi
    1e1c:	48 8b 70 70          	mov    rsi,QWORD PTR [rax+0x70]
    1e20:	48 8b 78 78          	mov    rdi,QWORD PTR [rax+0x78]
    1e24:	48 89 74 11 70       	mov    QWORD PTR [rcx+rdx*1+0x70],rsi
    1e29:	48 89 7c 11 78       	mov    QWORD PTR [rcx+rdx*1+0x78],rdi
    1e2e:	48 8b b0 80 00 00 00 	mov    rsi,QWORD PTR [rax+0x80]
    1e35:	48 8b b8 88 00 00 00 	mov    rdi,QWORD PTR [rax+0x88]
    1e3c:	48 89 b4 11 80 00 00 	mov    QWORD PTR [rcx+rdx*1+0x80],rsi
    1e43:	00 
    1e44:	48 89 bc 11 88 00 00 	mov    QWORD PTR [rcx+rdx*1+0x88],rdi
    1e4b:	00 
    1e4c:	48 8b b0 90 00 00 00 	mov    rsi,QWORD PTR [rax+0x90]
    1e53:	48 8b b8 98 00 00 00 	mov    rdi,QWORD PTR [rax+0x98]
    1e5a:	48 89 b4 11 90 00 00 	mov    QWORD PTR [rcx+rdx*1+0x90],rsi
    1e61:	00 
    1e62:	48 89 bc 11 98 00 00 	mov    QWORD PTR [rcx+rdx*1+0x98],rdi
    1e69:	00 
    1e6a:	48 8b b0 a0 00 00 00 	mov    rsi,QWORD PTR [rax+0xa0]
    1e71:	48 8b b8 a8 00 00 00 	mov    rdi,QWORD PTR [rax+0xa8]
    1e78:	48 89 b4 11 a0 00 00 	mov    QWORD PTR [rcx+rdx*1+0xa0],rsi
    1e7f:	00 
    1e80:	48 89 bc 11 a8 00 00 	mov    QWORD PTR [rcx+rdx*1+0xa8],rdi
    1e87:	00 
    1e88:	48 8b b0 b0 00 00 00 	mov    rsi,QWORD PTR [rax+0xb0]
    1e8f:	48 8b b8 b8 00 00 00 	mov    rdi,QWORD PTR [rax+0xb8]
    1e96:	48 89 b4 11 b0 00 00 	mov    QWORD PTR [rcx+rdx*1+0xb0],rsi
    1e9d:	00 
    1e9e:	48 89 bc 11 b8 00 00 	mov    QWORD PTR [rcx+rdx*1+0xb8],rdi
    1ea5:	00 
    1ea6:	48 8b b0 c0 00 00 00 	mov    rsi,QWORD PTR [rax+0xc0]
    1ead:	48 8b b8 c8 00 00 00 	mov    rdi,QWORD PTR [rax+0xc8]
    1eb4:	48 89 b4 11 c0 00 00 	mov    QWORD PTR [rcx+rdx*1+0xc0],rsi
    1ebb:	00 
    1ebc:	48 89 bc 11 c8 00 00 	mov    QWORD PTR [rcx+rdx*1+0xc8],rdi
    1ec3:	00 
    1ec4:	48 8b 80 d0 00 00 00 	mov    rax,QWORD PTR [rax+0xd0]
    1ecb:	48 89 84 11 d0 00 00 	mov    QWORD PTR [rcx+rdx*1+0xd0],rax
    1ed2:	00 
    1ed3:	90                   	nop
    1ed4:	5d                   	pop    rbp
    1ed5:	c3                   	ret

0000000000001ed6 <print_block>:
    1ed6:	f3 0f 1e fa          	endbr64
    1eda:	55                   	push   rbp
    1edb:	48 89 e5             	mov    rbp,rsp
    1ede:	48 83 ec 10          	sub    rsp,0x10
    1ee2:	48 89 7d f8          	mov    QWORD PTR [rbp-0x8],rdi
    1ee6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1eea:	48 8d b8 91 00 00 00 	lea    rdi,[rax+0x91]
    1ef1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1ef5:	8b b0 d4 00 00 00    	mov    esi,DWORD PTR [rax+0xd4]
    1efb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1eff:	48 8d 48 50          	lea    rcx,[rax+0x50]
    1f03:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1f07:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
    1f0b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1f0f:	8b 00                	mov    eax,DWORD PTR [rax]
    1f11:	48 83 ec 08          	sub    rsp,0x8
    1f15:	6a 40                	push   0x40
    1f17:	49 89 f9             	mov    r9,rdi
    1f1a:	41 89 f0             	mov    r8d,esi
    1f1d:	89 c6                	mov    esi,eax
    1f1f:	48 8d 05 82 12 00 00 	lea    rax,[rip+0x1282]        # 31a8 <_IO_stdin_used+0x1a8>
    1f26:	48 89 c7             	mov    rdi,rax
    1f29:	b8 00 00 00 00       	mov    eax,0x0
    1f2e:	e8 9d f2 ff ff       	call   11d0 <printf@plt>
    1f33:	48 83 c4 10          	add    rsp,0x10
    1f37:	90                   	nop
    1f38:	c9                   	leave
    1f39:	c3                   	ret

0000000000001f3a <main>:
    1f3a:	f3 0f 1e fa          	endbr64
    1f3e:	55                   	push   rbp
    1f3f:	48 89 e5             	mov    rbp,rsp
    1f42:	48 81 ec e0 06 00 00 	sub    rsp,0x6e0
    1f49:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    1f50:	00 00 
    1f52:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
    1f56:	31 c0                	xor    eax,eax
    1f58:	48 8b 05 c1 30 00 00 	mov    rax,QWORD PTR [rip+0x30c1]        # 5020 <stdout@GLIBC_2.2.5>
    1f5f:	b9 00 00 00 00       	mov    ecx,0x0
    1f64:	ba 02 00 00 00       	mov    edx,0x2
    1f69:	be 00 00 00 00       	mov    esi,0x0
    1f6e:	48 89 c7             	mov    rdi,rax
    1f71:	e8 4a f2 ff ff       	call   11c0 <setvbuf@plt>
    1f76:	48 8d 95 30 f9 ff ff 	lea    rdx,[rbp-0x6d0]
    1f7d:	b8 00 00 00 00       	mov    eax,0x0
    1f82:	b9 1b 00 00 00       	mov    ecx,0x1b
    1f87:	48 89 d7             	mov    rdi,rdx
    1f8a:	f3 48 ab             	rep stos QWORD PTR es:[rdi],rax
    1f8d:	c7 85 30 f9 ff ff 00 	mov    DWORD PTR [rbp-0x6d0],0x0
    1f94:	00 00 00 
    1f97:	bf 00 00 00 00       	mov    edi,0x0
    1f9c:	e8 af f2 ff ff       	call   1250 <time@plt>
    1fa1:	48 89 85 38 f9 ff ff 	mov    QWORD PTR [rbp-0x6c8],rax
    1fa8:	48 8d 85 30 f9 ff ff 	lea    rax,[rbp-0x6d0]
    1faf:	48 83 c0 50          	add    rax,0x50
    1fb3:	66 c7 00 30 00       	mov    WORD PTR [rax],0x30
    1fb8:	c7 85 04 fa ff ff 39 	mov    DWORD PTR [rbp-0x5fc],0x3039
    1fbf:	30 00 00 
    1fc2:	48 8d 85 30 f9 ff ff 	lea    rax,[rbp-0x6d0]
    1fc9:	48 83 c0 10          	add    rax,0x10
    1fcd:	ba 40 00 00 00       	mov    edx,0x40
    1fd2:	be 00 00 00 00       	mov    esi,0x0
    1fd7:	48 89 c7             	mov    rdi,rax
    1fda:	e8 41 f2 ff ff       	call   1220 <memset@plt>
    1fdf:	48 8d 85 30 f9 ff ff 	lea    rax,[rbp-0x6d0]
    1fe6:	48 89 c7             	mov    rdi,rax
    1fe9:	e8 d0 fa ff ff       	call   1abe <calculate_hash>
    1fee:	48 8d 85 30 f9 ff ff 	lea    rax,[rbp-0x6d0]
    1ff5:	48 89 c7             	mov    rdi,rax
    1ff8:	e8 50 fd ff ff       	call   1d4d <add_block>
    1ffd:	48 8d 05 24 12 00 00 	lea    rax,[rip+0x1224]        # 3228 <_IO_stdin_used+0x228>
    2004:	48 89 c7             	mov    rdi,rax
    2007:	e8 f4 f2 ff ff       	call   1300 <puts@plt>
    200c:	48 8d 85 30 f9 ff ff 	lea    rax,[rbp-0x6d0]
    2013:	48 89 c7             	mov    rdi,rax
    2016:	e8 bb fe ff ff       	call   1ed6 <print_block>
    201b:	48 8d 95 10 fa ff ff 	lea    rdx,[rbp-0x5f0]
    2022:	b8 00 00 00 00       	mov    eax,0x0
    2027:	b9 1b 00 00 00       	mov    ecx,0x1b
    202c:	48 89 d7             	mov    rdi,rdx
    202f:	f3 48 ab             	rep stos QWORD PTR es:[rdi],rax
    2032:	8b 05 78 38 00 00    	mov    eax,DWORD PTR [rip+0x3878]        # 58b0 <chain_len>
    2038:	83 e8 01             	sub    eax,0x1
    203b:	48 63 d0             	movsxd rdx,eax
    203e:	48 89 d0             	mov    rax,rdx
    2041:	48 01 c0             	add    rax,rax
    2044:	48 01 d0             	add    rax,rdx
    2047:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
    204e:	00 
    204f:	48 01 d0             	add    rax,rdx
    2052:	48 c1 e0 03          	shl    rax,0x3
    2056:	48 89 c2             	mov    rdx,rax
    2059:	48 8d 05 e0 2f 00 00 	lea    rax,[rip+0x2fe0]        # 5040 <blockchain>
    2060:	8b 04 02             	mov    eax,DWORD PTR [rdx+rax*1]
    2063:	83 c0 01             	add    eax,0x1
    2066:	89 85 10 fa ff ff    	mov    DWORD PTR [rbp-0x5f0],eax
    206c:	bf 00 00 00 00       	mov    edi,0x0
    2071:	e8 da f1 ff ff       	call   1250 <time@plt>
    2076:	48 89 85 18 fa ff ff 	mov    QWORD PTR [rbp-0x5e8],rax
    207d:	8b 05 2d 38 00 00    	mov    eax,DWORD PTR [rip+0x382d]        # 58b0 <chain_len>
    2083:	83 e8 01             	sub    eax,0x1
    2086:	48 63 d0             	movsxd rdx,eax
    2089:	48 89 d0             	mov    rax,rdx
    208c:	48 01 c0             	add    rax,rax
    208f:	48 01 d0             	add    rax,rdx
    2092:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
    2099:	00 
    209a:	48 01 d0             	add    rax,rdx
    209d:	48 c1 e0 03          	shl    rax,0x3
    20a1:	48 8d 90 90 00 00 00 	lea    rdx,[rax+0x90]
    20a8:	48 8d 05 91 2f 00 00 	lea    rax,[rip+0x2f91]        # 5040 <blockchain>
    20af:	48 01 d0             	add    rax,rdx
    20b2:	48 8d 50 01          	lea    rdx,[rax+0x1]
    20b6:	48 8d 85 10 fa ff ff 	lea    rax,[rbp-0x5f0]
    20bd:	48 83 c0 50          	add    rax,0x50
    20c1:	48 89 d6             	mov    rsi,rdx
    20c4:	48 89 c7             	mov    rdi,rax
    20c7:	e8 94 f1 ff ff       	call   1260 <strcpy@plt>
    20cc:	48 8d 05 a5 11 00 00 	lea    rax,[rip+0x11a5]        # 3278 <_IO_stdin_used+0x278>
    20d3:	48 89 c7             	mov    rdi,rax
    20d6:	e8 25 f2 ff ff       	call   1300 <puts@plt>
    20db:	48 8d 05 b4 11 00 00 	lea    rax,[rip+0x11b4]        # 3296 <_IO_stdin_used+0x296>
    20e2:	48 89 c7             	mov    rdi,rax
    20e5:	b8 00 00 00 00       	mov    eax,0x0
    20ea:	e8 e1 f0 ff ff       	call   11d0 <printf@plt>
    20ef:	48 8d 85 10 fa ff ff 	lea    rax,[rbp-0x5f0]
    20f6:	48 05 d4 00 00 00    	add    rax,0xd4
    20fc:	48 89 c6             	mov    rsi,rax
    20ff:	48 8d 05 a1 11 00 00 	lea    rax,[rip+0x11a1]        # 32a7 <_IO_stdin_used+0x2a7>
    2106:	48 89 c7             	mov    rdi,rax
    2109:	b8 00 00 00 00       	mov    eax,0x0
    210e:	e8 8d f1 ff ff       	call   12a0 <__isoc99_scanf@plt>
    2113:	e8 c8 f1 ff ff       	call   12e0 <getchar@plt>
    2118:	48 8d 05 91 11 00 00 	lea    rax,[rip+0x1191]        # 32b0 <_IO_stdin_used+0x2b0>
    211f:	48 89 c7             	mov    rdi,rax
    2122:	e8 d9 f1 ff ff       	call   1300 <puts@plt>
    2127:	48 8d 95 f0 fb ff ff 	lea    rdx,[rbp-0x410]
    212e:	b8 00 00 00 00       	mov    eax,0x0
    2133:	b9 80 00 00 00       	mov    ecx,0x80
    2138:	48 89 d7             	mov    rdi,rdx
    213b:	f3 48 ab             	rep stos QWORD PTR es:[rdi],rax
    213e:	eb 4d                	jmp    218d <main+0x253>
    2140:	48 8d 85 f0 fa ff ff 	lea    rax,[rbp-0x510]
    2147:	48 8d 15 9f 0f 00 00 	lea    rdx,[rip+0xf9f]        # 30ed <_IO_stdin_used+0xed>
    214e:	48 89 d6             	mov    rsi,rdx
    2151:	48 89 c7             	mov    rdi,rax
    2154:	e8 97 f1 ff ff       	call   12f0 <strcmp@plt>
    2159:	85 c0                	test   eax,eax
    215b:	74 52                	je     21af <main+0x275>
    215d:	48 8d 85 f0 fb ff ff 	lea    rax,[rbp-0x410]
    2164:	48 89 c7             	mov    rdi,rax
    2167:	e8 94 f0 ff ff       	call   1200 <strlen@plt>
    216c:	ba ff 03 00 00       	mov    edx,0x3ff
    2171:	48 29 c2             	sub    rdx,rax
    2174:	48 8d 8d f0 fa ff ff 	lea    rcx,[rbp-0x510]
    217b:	48 8d 85 f0 fb ff ff 	lea    rax,[rbp-0x410]
    2182:	48 89 ce             	mov    rsi,rcx
    2185:	48 89 c7             	mov    rdi,rax
    2188:	e8 a3 f0 ff ff       	call   1230 <strncat@plt>
    218d:	48 8b 15 9c 2e 00 00 	mov    rdx,QWORD PTR [rip+0x2e9c]        # 5030 <stdin@GLIBC_2.2.5>
    2194:	48 8d 85 f0 fa ff ff 	lea    rax,[rbp-0x510]
    219b:	be 00 01 00 00       	mov    esi,0x100
    21a0:	48 89 c7             	mov    rdi,rax
    21a3:	e8 78 f1 ff ff       	call   1320 <fgets@plt>
    21a8:	48 85 c0             	test   rax,rax
    21ab:	75 93                	jne    2140 <main+0x206>
    21ad:	eb 01                	jmp    21b0 <main+0x276>
    21af:	90                   	nop
    21b0:	48 8d 85 10 fa ff ff 	lea    rax,[rbp-0x5f0]
    21b7:	48 8d 50 10          	lea    rdx,[rax+0x10]
    21bb:	48 8d 85 f0 fb ff ff 	lea    rax,[rbp-0x410]
    21c2:	48 89 d6             	mov    rsi,rdx
    21c5:	48 89 c7             	mov    rdi,rax
    21c8:	e8 9b f6 ff ff       	call   1868 <assemble_rv_code>
    21cd:	89 85 2c f9 ff ff    	mov    DWORD PTR [rbp-0x6d4],eax
    21d3:	83 bd 2c f9 ff ff 00 	cmp    DWORD PTR [rbp-0x6d4],0x0
    21da:	79 19                	jns    21f5 <main+0x2bb>
    21dc:	48 8d 05 0d 11 00 00 	lea    rax,[rip+0x110d]        # 32f0 <_IO_stdin_used+0x2f0>
    21e3:	48 89 c7             	mov    rdi,rax
    21e6:	e8 15 f1 ff ff       	call   1300 <puts@plt>
    21eb:	b8 01 00 00 00       	mov    eax,0x1
    21f0:	e9 c5 00 00 00       	jmp    22ba <main+0x380>
    21f5:	8b 85 2c f9 ff ff    	mov    eax,DWORD PTR [rbp-0x6d4]
    21fb:	89 c6                	mov    esi,eax
    21fd:	48 8d 05 14 11 00 00 	lea    rax,[rip+0x1114]        # 3318 <_IO_stdin_used+0x318>
    2204:	48 89 c7             	mov    rdi,rax
    2207:	b8 00 00 00 00       	mov    eax,0x0
    220c:	e8 bf ef ff ff       	call   11d0 <printf@plt>
    2211:	48 8d 85 10 fa ff ff 	lea    rax,[rbp-0x5f0]
    2218:	48 89 c7             	mov    rdi,rax
    221b:	e8 9e f8 ff ff       	call   1abe <calculate_hash>
    2220:	8b 05 8a 36 00 00    	mov    eax,DWORD PTR [rip+0x368a]        # 58b0 <chain_len>
    2226:	83 e8 01             	sub    eax,0x1
    2229:	48 63 d0             	movsxd rdx,eax
    222c:	48 89 d0             	mov    rax,rdx
    222f:	48 01 c0             	add    rax,rax
    2232:	48 01 d0             	add    rax,rdx
    2235:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
    223c:	00 
    223d:	48 01 d0             	add    rax,rdx
    2240:	48 c1 e0 03          	shl    rax,0x3
    2244:	48 8d 15 f5 2d 00 00 	lea    rdx,[rip+0x2df5]        # 5040 <blockchain>
    224b:	48 01 c2             	add    rdx,rax
    224e:	48 8d 85 10 fa ff ff 	lea    rax,[rbp-0x5f0]
    2255:	48 89 d6             	mov    rsi,rdx
    2258:	48 89 c7             	mov    rdi,rax
    225b:	e8 e6 f9 ff ff       	call   1c46 <is_block_valid>
    2260:	85 c0                	test   eax,eax
    2262:	74 42                	je     22a6 <main+0x36c>
    2264:	48 8d 05 dd 10 00 00 	lea    rax,[rip+0x10dd]        # 3348 <_IO_stdin_used+0x348>
    226b:	48 89 c7             	mov    rdi,rax
    226e:	e8 8d f0 ff ff       	call   1300 <puts@plt>
    2273:	48 8d 85 10 fa ff ff 	lea    rax,[rbp-0x5f0]
    227a:	48 89 c7             	mov    rdi,rax
    227d:	e8 cb fa ff ff       	call   1d4d <add_block>
    2282:	48 8d 85 10 fa ff ff 	lea    rax,[rbp-0x5f0]
    2289:	48 89 c7             	mov    rdi,rax
    228c:	e8 45 fc ff ff       	call   1ed6 <print_block>
    2291:	48 8d 85 10 fa ff ff 	lea    rax,[rbp-0x5f0]
    2298:	48 83 c0 10          	add    rax,0x10
    229c:	48 89 c7             	mov    rdi,rax
    229f:	e8 7b f2 ff ff       	call   151f <execute_rv_code>
    22a4:	eb 0f                	jmp    22b5 <main+0x37b>
    22a6:	48 8d 05 c3 10 00 00 	lea    rax,[rip+0x10c3]        # 3370 <_IO_stdin_used+0x370>
    22ad:	48 89 c7             	mov    rdi,rax
    22b0:	e8 4b f0 ff ff       	call   1300 <puts@plt>
    22b5:	b8 00 00 00 00       	mov    eax,0x0
    22ba:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
    22be:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    22c5:	00 00 
    22c7:	74 05                	je     22ce <main+0x394>
    22c9:	e8 c2 ef ff ff       	call   1290 <__stack_chk_fail@plt>
    22ce:	c9                   	leave
    22cf:	c3                   	ret

Disassembly of section .fini:

00000000000022d0 <_fini>:
    22d0:	f3 0f 1e fa          	endbr64
    22d4:	48 83 ec 08          	sub    rsp,0x8
    22d8:	48 83 c4 08          	add    rsp,0x8
    22dc:	c3                   	ret
