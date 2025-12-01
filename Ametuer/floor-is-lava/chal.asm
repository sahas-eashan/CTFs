
chal:     file format elf64-x86-64


Disassembly of section .init:

0000000000001000 <.init>:
    1000:	f3 0f 1e fa          	endbr64
    1004:	48 83 ec 08          	sub    rsp,0x8
    1008:	48 8b 05 d9 2f 00 00 	mov    rax,QWORD PTR [rip+0x2fd9]        # 3fe8 <rand@plt+0x2ef8>
    100f:	48 85 c0             	test   rax,rax
    1012:	74 02                	je     1016 <__cxa_finalize@plt-0x7a>
    1014:	ff d0                	call   rax
    1016:	48 83 c4 08          	add    rsp,0x8
    101a:	c3                   	ret

Disassembly of section .plt:

0000000000001020 <.plt>:
    1020:	ff 35 72 2f 00 00    	push   QWORD PTR [rip+0x2f72]        # 3f98 <rand@plt+0x2ea8>
    1026:	ff 25 74 2f 00 00    	jmp    QWORD PTR [rip+0x2f74]        # 3fa0 <rand@plt+0x2eb0>
    102c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    1030:	f3 0f 1e fa          	endbr64
    1034:	68 00 00 00 00       	push   0x0
    1039:	e9 e2 ff ff ff       	jmp    1020 <__cxa_finalize@plt-0x70>
    103e:	66 90                	xchg   ax,ax
    1040:	f3 0f 1e fa          	endbr64
    1044:	68 01 00 00 00       	push   0x1
    1049:	e9 d2 ff ff ff       	jmp    1020 <__cxa_finalize@plt-0x70>
    104e:	66 90                	xchg   ax,ax
    1050:	f3 0f 1e fa          	endbr64
    1054:	68 02 00 00 00       	push   0x2
    1059:	e9 c2 ff ff ff       	jmp    1020 <__cxa_finalize@plt-0x70>
    105e:	66 90                	xchg   ax,ax
    1060:	f3 0f 1e fa          	endbr64
    1064:	68 03 00 00 00       	push   0x3
    1069:	e9 b2 ff ff ff       	jmp    1020 <__cxa_finalize@plt-0x70>
    106e:	66 90                	xchg   ax,ax
    1070:	f3 0f 1e fa          	endbr64
    1074:	68 04 00 00 00       	push   0x4
    1079:	e9 a2 ff ff ff       	jmp    1020 <__cxa_finalize@plt-0x70>
    107e:	66 90                	xchg   ax,ax
    1080:	f3 0f 1e fa          	endbr64
    1084:	68 05 00 00 00       	push   0x5
    1089:	e9 92 ff ff ff       	jmp    1020 <__cxa_finalize@plt-0x70>
    108e:	66 90                	xchg   ax,ax

Disassembly of section .plt.got:

0000000000001090 <__cxa_finalize@plt>:
    1090:	f3 0f 1e fa          	endbr64
    1094:	ff 25 5e 2f 00 00    	jmp    QWORD PTR [rip+0x2f5e]        # 3ff8 <rand@plt+0x2f08>
    109a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .plt.sec:

00000000000010a0 <puts@plt>:
    10a0:	f3 0f 1e fa          	endbr64
    10a4:	ff 25 fe 2e 00 00    	jmp    QWORD PTR [rip+0x2efe]        # 3fa8 <rand@plt+0x2eb8>
    10aa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000010b0 <__stack_chk_fail@plt>:
    10b0:	f3 0f 1e fa          	endbr64
    10b4:	ff 25 f6 2e 00 00    	jmp    QWORD PTR [rip+0x2ef6]        # 3fb0 <rand@plt+0x2ec0>
    10ba:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000010c0 <printf@plt>:
    10c0:	f3 0f 1e fa          	endbr64
    10c4:	ff 25 ee 2e 00 00    	jmp    QWORD PTR [rip+0x2eee]        # 3fb8 <rand@plt+0x2ec8>
    10ca:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000010d0 <srand@plt>:
    10d0:	f3 0f 1e fa          	endbr64
    10d4:	ff 25 e6 2e 00 00    	jmp    QWORD PTR [rip+0x2ee6]        # 3fc0 <rand@plt+0x2ed0>
    10da:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000010e0 <getchar@plt>:
    10e0:	f3 0f 1e fa          	endbr64
    10e4:	ff 25 de 2e 00 00    	jmp    QWORD PTR [rip+0x2ede]        # 3fc8 <rand@plt+0x2ed8>
    10ea:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000010f0 <rand@plt>:
    10f0:	f3 0f 1e fa          	endbr64
    10f4:	ff 25 d6 2e 00 00    	jmp    QWORD PTR [rip+0x2ed6]        # 3fd0 <rand@plt+0x2ee0>
    10fa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .text:

0000000000001100 <.text>:
    1100:	f3 0f 1e fa          	endbr64
    1104:	31 ed                	xor    ebp,ebp
    1106:	49 89 d1             	mov    r9,rdx
    1109:	5e                   	pop    rsi
    110a:	48 89 e2             	mov    rdx,rsp
    110d:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
    1111:	50                   	push   rax
    1112:	54                   	push   rsp
    1113:	45 31 c0             	xor    r8d,r8d
    1116:	31 c9                	xor    ecx,ecx
    1118:	48 8d 3d ca 00 00 00 	lea    rdi,[rip+0xca]        # 11e9 <rand@plt+0xf9>
    111f:	ff 15 b3 2e 00 00    	call   QWORD PTR [rip+0x2eb3]        # 3fd8 <rand@plt+0x2ee8>
    1125:	f4                   	hlt
    1126:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    112d:	00 00 00 
    1130:	48 8d 3d 09 2f 00 00 	lea    rdi,[rip+0x2f09]        # 4040 <rand@plt+0x2f50>
    1137:	48 8d 05 02 2f 00 00 	lea    rax,[rip+0x2f02]        # 4040 <rand@plt+0x2f50>
    113e:	48 39 f8             	cmp    rax,rdi
    1141:	74 15                	je     1158 <rand@plt+0x68>
    1143:	48 8b 05 96 2e 00 00 	mov    rax,QWORD PTR [rip+0x2e96]        # 3fe0 <rand@plt+0x2ef0>
    114a:	48 85 c0             	test   rax,rax
    114d:	74 09                	je     1158 <rand@plt+0x68>
    114f:	ff e0                	jmp    rax
    1151:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    1158:	c3                   	ret
    1159:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    1160:	48 8d 3d d9 2e 00 00 	lea    rdi,[rip+0x2ed9]        # 4040 <rand@plt+0x2f50>
    1167:	48 8d 35 d2 2e 00 00 	lea    rsi,[rip+0x2ed2]        # 4040 <rand@plt+0x2f50>
    116e:	48 29 fe             	sub    rsi,rdi
    1171:	48 89 f0             	mov    rax,rsi
    1174:	48 c1 ee 3f          	shr    rsi,0x3f
    1178:	48 c1 f8 03          	sar    rax,0x3
    117c:	48 01 c6             	add    rsi,rax
    117f:	48 d1 fe             	sar    rsi,1
    1182:	74 14                	je     1198 <rand@plt+0xa8>
    1184:	48 8b 05 65 2e 00 00 	mov    rax,QWORD PTR [rip+0x2e65]        # 3ff0 <rand@plt+0x2f00>
    118b:	48 85 c0             	test   rax,rax
    118e:	74 08                	je     1198 <rand@plt+0xa8>
    1190:	ff e0                	jmp    rax
    1192:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    1198:	c3                   	ret
    1199:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    11a0:	f3 0f 1e fa          	endbr64
    11a4:	80 3d 95 2e 00 00 00 	cmp    BYTE PTR [rip+0x2e95],0x0        # 4040 <rand@plt+0x2f50>
    11ab:	75 2b                	jne    11d8 <rand@plt+0xe8>
    11ad:	55                   	push   rbp
    11ae:	48 83 3d 42 2e 00 00 	cmp    QWORD PTR [rip+0x2e42],0x0        # 3ff8 <rand@plt+0x2f08>
    11b5:	00 
    11b6:	48 89 e5             	mov    rbp,rsp
    11b9:	74 0c                	je     11c7 <rand@plt+0xd7>
    11bb:	48 8b 3d 46 2e 00 00 	mov    rdi,QWORD PTR [rip+0x2e46]        # 4008 <rand@plt+0x2f18>
    11c2:	e8 c9 fe ff ff       	call   1090 <__cxa_finalize@plt>
    11c7:	e8 64 ff ff ff       	call   1130 <rand@plt+0x40>
    11cc:	c6 05 6d 2e 00 00 01 	mov    BYTE PTR [rip+0x2e6d],0x1        # 4040 <rand@plt+0x2f50>
    11d3:	5d                   	pop    rbp
    11d4:	c3                   	ret
    11d5:	0f 1f 00             	nop    DWORD PTR [rax]
    11d8:	c3                   	ret
    11d9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    11e0:	f3 0f 1e fa          	endbr64
    11e4:	e9 77 ff ff ff       	jmp    1160 <rand@plt+0x70>
    11e9:	f3 0f 1e fa          	endbr64
    11ed:	55                   	push   rbp
    11ee:	48 89 e5             	mov    rbp,rsp
    11f1:	48 83 ec 30          	sub    rsp,0x30
    11f5:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    11fc:	00 00 
    11fe:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
    1202:	31 c0                	xor    eax,eax
    1204:	c7 45 e0 00 00 00 00 	mov    DWORD PTR [rbp-0x20],0x0
    120b:	e9 4c 01 00 00       	jmp    135c <rand@plt+0x26c>
    1210:	48 8d 05 ed 0d 00 00 	lea    rax,[rip+0xded]        # 2004 <rand@plt+0xf14>
    1217:	48 89 c7             	mov    rdi,rax
    121a:	b8 00 00 00 00       	mov    eax,0x0
    121f:	e8 9c fe ff ff       	call   10c0 <printf@plt>
    1224:	e8 b7 fe ff ff       	call   10e0 <getchar@plt>
    1229:	88 45 df             	mov    BYTE PTR [rbp-0x21],al
    122c:	80 7d df 0a          	cmp    BYTE PTR [rbp-0x21],0xa
    1230:	74 f2                	je     1224 <rand@plt+0x134>
    1232:	80 7d df 77          	cmp    BYTE PTR [rbp-0x21],0x77
    1236:	75 2a                	jne    1262 <rand@plt+0x172>
    1238:	0f b6 05 12 2e 00 00 	movzx  eax,BYTE PTR [rip+0x2e12]        # 4051 <rand@plt+0x2f61>
    123f:	83 e8 01             	sub    eax,0x1
    1242:	88 05 09 2e 00 00    	mov    BYTE PTR [rip+0x2e09],al        # 4051 <rand@plt+0x2f61>
    1248:	48 8b 05 e9 2d 00 00 	mov    rax,QWORD PTR [rip+0x2de9]        # 4038 <rand@plt+0x2f48>
    124f:	48 8d 50 01          	lea    rdx,[rax+0x1]
    1253:	48 89 15 de 2d 00 00 	mov    QWORD PTR [rip+0x2dde],rdx        # 4038 <rand@plt+0x2f48>
    125a:	c6 00 00             	mov    BYTE PTR [rax],0x0
    125d:	e9 89 00 00 00       	jmp    12eb <rand@plt+0x1fb>
    1262:	80 7d df 61          	cmp    BYTE PTR [rbp-0x21],0x61
    1266:	75 27                	jne    128f <rand@plt+0x19f>
    1268:	0f b6 05 e1 2d 00 00 	movzx  eax,BYTE PTR [rip+0x2de1]        # 4050 <rand@plt+0x2f60>
    126f:	83 e8 01             	sub    eax,0x1
    1272:	88 05 d8 2d 00 00    	mov    BYTE PTR [rip+0x2dd8],al        # 4050 <rand@plt+0x2f60>
    1278:	48 8b 05 b9 2d 00 00 	mov    rax,QWORD PTR [rip+0x2db9]        # 4038 <rand@plt+0x2f48>
    127f:	48 8d 50 01          	lea    rdx,[rax+0x1]
    1283:	48 89 15 ae 2d 00 00 	mov    QWORD PTR [rip+0x2dae],rdx        # 4038 <rand@plt+0x2f48>
    128a:	c6 00 01             	mov    BYTE PTR [rax],0x1
    128d:	eb 5c                	jmp    12eb <rand@plt+0x1fb>
    128f:	80 7d df 73          	cmp    BYTE PTR [rbp-0x21],0x73
    1293:	75 27                	jne    12bc <rand@plt+0x1cc>
    1295:	0f b6 05 b5 2d 00 00 	movzx  eax,BYTE PTR [rip+0x2db5]        # 4051 <rand@plt+0x2f61>
    129c:	83 c0 01             	add    eax,0x1
    129f:	88 05 ac 2d 00 00    	mov    BYTE PTR [rip+0x2dac],al        # 4051 <rand@plt+0x2f61>
    12a5:	48 8b 05 8c 2d 00 00 	mov    rax,QWORD PTR [rip+0x2d8c]        # 4038 <rand@plt+0x2f48>
    12ac:	48 8d 50 01          	lea    rdx,[rax+0x1]
    12b0:	48 89 15 81 2d 00 00 	mov    QWORD PTR [rip+0x2d81],rdx        # 4038 <rand@plt+0x2f48>
    12b7:	c6 00 02             	mov    BYTE PTR [rax],0x2
    12ba:	eb 2f                	jmp    12eb <rand@plt+0x1fb>
    12bc:	80 7d df 64          	cmp    BYTE PTR [rbp-0x21],0x64
    12c0:	0f 85 95 00 00 00    	jne    135b <rand@plt+0x26b>
    12c6:	0f b6 05 83 2d 00 00 	movzx  eax,BYTE PTR [rip+0x2d83]        # 4050 <rand@plt+0x2f60>
    12cd:	83 c0 01             	add    eax,0x1
    12d0:	88 05 7a 2d 00 00    	mov    BYTE PTR [rip+0x2d7a],al        # 4050 <rand@plt+0x2f60>
    12d6:	48 8b 05 5b 2d 00 00 	mov    rax,QWORD PTR [rip+0x2d5b]        # 4038 <rand@plt+0x2f48>
    12dd:	48 8d 50 01          	lea    rdx,[rax+0x1]
    12e1:	48 89 15 50 2d 00 00 	mov    QWORD PTR [rip+0x2d50],rdx        # 4038 <rand@plt+0x2f48>
    12e8:	c6 00 03             	mov    BYTE PTR [rax],0x3
    12eb:	0f b6 05 5e 2d 00 00 	movzx  eax,BYTE PTR [rip+0x2d5e]        # 4050 <rand@plt+0x2f60>
    12f2:	83 e0 07             	and    eax,0x7
    12f5:	88 05 55 2d 00 00    	mov    BYTE PTR [rip+0x2d55],al        # 4050 <rand@plt+0x2f60>
    12fb:	0f b6 05 4f 2d 00 00 	movzx  eax,BYTE PTR [rip+0x2d4f]        # 4051 <rand@plt+0x2f61>
    1302:	83 e0 07             	and    eax,0x7
    1305:	88 05 46 2d 00 00    	mov    BYTE PTR [rip+0x2d46],al        # 4051 <rand@plt+0x2f61>
    130b:	0f b6 05 3f 2d 00 00 	movzx  eax,BYTE PTR [rip+0x2d3f]        # 4051 <rand@plt+0x2f61>
    1312:	0f b6 c0             	movzx  eax,al
    1315:	48 98                	cdqe
    1317:	48 8d 15 f2 2c 00 00 	lea    rdx,[rip+0x2cf2]        # 4010 <rand@plt+0x2f20>
    131e:	0f b6 04 10          	movzx  eax,BYTE PTR [rax+rdx*1]
    1322:	89 c6                	mov    esi,eax
    1324:	0f b6 05 25 2d 00 00 	movzx  eax,BYTE PTR [rip+0x2d25]        # 4050 <rand@plt+0x2f60>
    132b:	0f b6 c0             	movzx  eax,al
    132e:	ba 01 00 00 00       	mov    edx,0x1
    1333:	89 c1                	mov    ecx,eax
    1335:	d3 e2                	shl    edx,cl
    1337:	89 d0                	mov    eax,edx
    1339:	31 c6                	xor    esi,eax
    133b:	89 f2                	mov    edx,esi
    133d:	0f b6 05 0d 2d 00 00 	movzx  eax,BYTE PTR [rip+0x2d0d]        # 4051 <rand@plt+0x2f61>
    1344:	0f b6 c0             	movzx  eax,al
    1347:	89 d1                	mov    ecx,edx
    1349:	48 98                	cdqe
    134b:	48 8d 15 be 2c 00 00 	lea    rdx,[rip+0x2cbe]        # 4010 <rand@plt+0x2f20>
    1352:	88 0c 10             	mov    BYTE PTR [rax+rdx*1],cl
    1355:	83 45 e0 01          	add    DWORD PTR [rbp-0x20],0x1
    1359:	eb 01                	jmp    135c <rand@plt+0x26c>
    135b:	90                   	nop
    135c:	83 7d e0 1b          	cmp    DWORD PTR [rbp-0x20],0x1b
    1360:	0f 8e aa fe ff ff    	jle    1210 <rand@plt+0x120>
    1366:	c7 45 e4 00 00 00 00 	mov    DWORD PTR [rbp-0x1c],0x0
    136d:	eb 51                	jmp    13c0 <rand@plt+0x2d0>
    136f:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
    1372:	69 c0 37 13 00 00    	imul   eax,eax,0x1337
    1378:	2d 11 41 52 21       	sub    eax,0x21524111
    137d:	89 c7                	mov    edi,eax
    137f:	e8 4c fd ff ff       	call   10d0 <srand@plt>
    1384:	e8 67 fd ff ff       	call   10f0 <rand@plt>
    1389:	0f b6 d0             	movzx  edx,al
    138c:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
    138f:	48 98                	cdqe
    1391:	48 8d 0d 78 2c 00 00 	lea    rcx,[rip+0x2c78]        # 4010 <rand@plt+0x2f20>
    1398:	0f b6 04 08          	movzx  eax,BYTE PTR [rax+rcx*1]
    139c:	0f b6 c0             	movzx  eax,al
    139f:	39 c2                	cmp    edx,eax
    13a1:	74 19                	je     13bc <rand@plt+0x2cc>
    13a3:	48 8d 05 5d 0c 00 00 	lea    rax,[rip+0xc5d]        # 2007 <rand@plt+0xf17>
    13aa:	48 89 c7             	mov    rdi,rax
    13ad:	e8 ee fc ff ff       	call   10a0 <puts@plt>
    13b2:	b8 00 00 00 00       	mov    eax,0x0
    13b7:	e9 e9 00 00 00       	jmp    14a5 <rand@plt+0x3b5>
    13bc:	83 45 e4 01          	add    DWORD PTR [rbp-0x1c],0x1
    13c0:	83 7d e4 07          	cmp    DWORD PTR [rbp-0x1c],0x7
    13c4:	7e a9                	jle    136f <rand@plt+0x27f>
    13c6:	48 c7 45 f0 00 00 00 	mov    QWORD PTR [rbp-0x10],0x0
    13cd:	00 
    13ce:	c7 45 e8 00 00 00 00 	mov    DWORD PTR [rbp-0x18],0x0
    13d5:	eb 2a                	jmp    1401 <rand@plt+0x311>
    13d7:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
    13db:	48 8d 0c 85 00 00 00 	lea    rcx,[rax*4+0x0]
    13e2:	00 
    13e3:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
    13e6:	48 98                	cdqe
    13e8:	48 8d 15 71 2c 00 00 	lea    rdx,[rip+0x2c71]        # 4060 <rand@plt+0x2f70>
    13ef:	0f b6 04 10          	movzx  eax,BYTE PTR [rax+rdx*1]
    13f3:	0f b6 c0             	movzx  eax,al
    13f6:	48 09 c8             	or     rax,rcx
    13f9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
    13fd:	83 45 e8 01          	add    DWORD PTR [rbp-0x18],0x1
    1401:	83 7d e8 1b          	cmp    DWORD PTR [rbp-0x18],0x1b
    1405:	7e d0                	jle    13d7 <rand@plt+0x2e7>
    1407:	48 8d 45 f0          	lea    rax,[rbp-0x10]
    140b:	8b 10                	mov    edx,DWORD PTR [rax]
    140d:	48 8d 45 f0          	lea    rax,[rbp-0x10]
    1411:	48 83 c0 04          	add    rax,0x4
    1415:	8b 00                	mov    eax,DWORD PTR [rax]
    1417:	31 d0                	xor    eax,edx
    1419:	89 c7                	mov    edi,eax
    141b:	e8 b0 fc ff ff       	call   10d0 <srand@plt>
    1420:	c7 45 ec 00 00 00 00 	mov    DWORD PTR [rbp-0x14],0x0
    1427:	eb 33                	jmp    145c <rand@plt+0x36c>
    1429:	e8 c2 fc ff ff       	call   10f0 <rand@plt>
    142e:	0f b6 c8             	movzx  ecx,al
    1431:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
    1434:	48 98                	cdqe
    1436:	48 8d 15 e3 2b 00 00 	lea    rdx,[rip+0x2be3]        # 4020 <rand@plt+0x2f30>
    143d:	0f b6 04 10          	movzx  eax,BYTE PTR [rax+rdx*1]
    1441:	89 c2                	mov    edx,eax
    1443:	89 c8                	mov    eax,ecx
    1445:	31 d0                	xor    eax,edx
    1447:	89 c1                	mov    ecx,eax
    1449:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
    144c:	48 98                	cdqe
    144e:	48 8d 15 cb 2b 00 00 	lea    rdx,[rip+0x2bcb]        # 4020 <rand@plt+0x2f30>
    1455:	88 0c 10             	mov    BYTE PTR [rax+rdx*1],cl
    1458:	83 45 ec 01          	add    DWORD PTR [rbp-0x14],0x1
    145c:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
    145f:	83 f8 14             	cmp    eax,0x14
    1462:	76 c5                	jbe    1429 <rand@plt+0x339>
    1464:	48 8d 05 af 0b 00 00 	lea    rax,[rip+0xbaf]        # 201a <rand@plt+0xf2a>
    146b:	48 89 c7             	mov    rdi,rax
    146e:	e8 2d fc ff ff       	call   10a0 <puts@plt>
    1473:	48 8d 05 b4 0b 00 00 	lea    rax,[rip+0xbb4]        # 202e <rand@plt+0xf3e>
    147a:	48 89 c7             	mov    rdi,rax
    147d:	e8 1e fc ff ff       	call   10a0 <puts@plt>
    1482:	48 8d 05 97 2b 00 00 	lea    rax,[rip+0x2b97]        # 4020 <rand@plt+0x2f30>
    1489:	48 89 c6             	mov    rsi,rax
    148c:	48 8d 05 af 0b 00 00 	lea    rax,[rip+0xbaf]        # 2042 <rand@plt+0xf52>
    1493:	48 89 c7             	mov    rdi,rax
    1496:	b8 00 00 00 00       	mov    eax,0x0
    149b:	e8 20 fc ff ff       	call   10c0 <printf@plt>
    14a0:	b8 00 00 00 00       	mov    eax,0x0
    14a5:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
    14a9:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    14b0:	00 00 
    14b2:	74 05                	je     14b9 <rand@plt+0x3c9>
    14b4:	e8 f7 fb ff ff       	call   10b0 <__stack_chk_fail@plt>
    14b9:	c9                   	leave
    14ba:	c3                   	ret

Disassembly of section .fini:

00000000000014bc <.fini>:
    14bc:	f3 0f 1e fa          	endbr64
    14c0:	48 83 ec 08          	sub    rsp,0x8
    14c4:	48 83 c4 08          	add    rsp,0x8
    14c8:	c3                   	ret
