import base92
import struct

# Your Base92 string (from your prompt)
encoded_str = r"""6L#deR,X:sUZ=ZOK=-/L-W-n4,H)?Dd=@Cj6>JWqh/Yd<^Zc14%Qjw_gc(hkA&gb9c:Nh3-=hII_pT+L5+t|\,+e;#C>'D*}A!t@U&+u.LIP?ulg?9hCy,0/.0ag+I0T?Z^3\&X#UfC6V7rR:AvfrBcxm{Ho<5gV6R\zEcYkn/Q@S{G/>7t@1b*amDGRn|(5J3R;i[cXPLH-p=0]9<;ilC4_(X^^Y&gE5(thp_1d[AJ=*K<55H1)z^+fsThrkLR8CPF3cy3[3zj|X{3PF_:'0F^q@^LBA_!U4B/@YJ[sP.qyVxjM?;RwrAY)#1KY@s0p631RAK,8K/[o=L?-<Lswe@0[b1UNmvzp<K;4a53l?jSEj@%F=0/P8l_Vl|^fXQdZAjGlvR/E@HIXk<(X3Cs[38,6skOx<nLxF^F;6)0-#5ITn}%J3D&[A8Xs9bUNp5RvCNH--Z^AKl[)SyRy8T;?p_3M$!GX({x%5KT$a=YhE[nMSzGf?}QFBT2x4.Wcl)DCI1%.ST/6[xs@j/D6IL:S!V[2gy[;kliqJsh3t}Y8n3H|UD<D6,1oa?Xt:*LE=[AE2?h|o5]_D{o&>hU:=2/hfnbPn[T*U[(fCMv^OH25[veE;Pip?a\}sX1?hEIY>86U6Kuad6Y+[?pVkEJ;H)he,8V*r|I]n|dBDXhKzQbAUhQ9AGuXBI:O[s0;(^QG(9dt3f[tv7-^EWJ6Ag<55+H@_-,6s}cy=e+I<q$M7JV{x]m,@Blg5IF_6#V9\^NLWwA?HGEbYO5$P2e}SirQJv0qto^RJ{M/S1dK6L#hVRYY5A@P'&<EBL$0dA0\.PEH(:J#3a2;33bCsqa&o8U!G!&d&jYX(^l9jNgGHm<@p{0<.BIY>0lm3<t@VI,8Z}L@=s3e9b/leF5FggXJA.6=Hj&OPf_wJ,Ra)&Ub@^t8S[*nUfHzV7d@0M:Vp{[3KdHn@KB56,:wo>+u(^ZPSyUP5IhaVP0kP:F'kELq:'S<6#/8sij3jNa^F]&k^c]\Ufov<%ir:>j5t}6;5#J6jFJX732'SaXgs@a#=l.AIRh}_,(5gatp;PRKF_:?I^.ThlFe(lUv7sEc1|2%Q?CySyoI@bi8r5[u[vDW)W(c5k^sq|XUDmop&rLz8}s|-[1/gg[(S1I}5p[|wc+5i*iMV_zx8x%Q\=2f)lO-XIjO3%1Yv6d-!kJ}Y/r\6lSy3O+e;#GR<p3M.*$Q34YXs&T2B\RJ>W=6eJ_HcBo+p=.D:b%V;m/g[?WYW$lz4D0\sg3n/=J6@t+>5NQ^V:XUJD[-=[B)A)FB[y(u#5IRXS+$J/&NSS4b#A=X@I3i6-%Qjwa;c([h@)dt7PF.vRaMQKI_j/0{3<sxN%+txj;R&H6W.D/hg0VIgXj<@CAW;+F/A90-x?J8)&UC=O/4BT(#Udl}?}rNE9;Wu/,&UxJ}m/Rh5oG3SfYkh#c5'.63>z\M-RUT9f[:XdDD>5Gq7G0*Q#J7kM-_=q;\a-0+c&k'*Sgb0NG#v5\FawJD=$3b5+t3e\Xv)7_EkSX$CSh}[|Z=D{IY*lg0;,=Ad!12s*SE+AlS;g;mL_'oUfH}U2p&5-SSt{a.awIYB-DQ6/i8ZjY(/b>E=SDm1W:wn'(TUp\QW5rHE60rFs5&hrc0n{dn>4uL\:/&h#GRnsjMHm<Tv7UCPyIR=dlt5H&?fl+fg^BOT7(JH&QVV7)kUtl}+1znG!'+paa>JXdUUKU%2X_H&a0+UfIX?}UH>u0(r'YG)%KhjO3c5o/@0?*aExQ|&pgZ2^\ba65v#7nU=!aUC+:[0D/z4F]8(*.0GB%Fix+sKnL@W,g+6r^&secV3]J|oyx16lG\('Xt@&XJjoL\Gat4=$2wx[Xzo(6=I1%wK,.T/?LB(zxX;F^?(-_6P0TrnRapAkS+sJbCyBJ|pf[Q6OGu;yW]x_h+=RWx4J:|8x*?#9jq;b*|F<F&r)+19O]7<p9F<K;h^}4OPif(?Ll\ImR:p_+Q[pJ=?%O|6,G8lYXdP2a'=KRJ8zhy=6U6#?OxQx+'5&sdD%.QE9GIA_>TAdt8,Bd:VBnIpealIqHir(*=/;KY@rGA6Rha&g,FV@J:&q[P@bi4SY^B[QF)j/O^CU&FlJcD:*afQw.;:b/P,7TpJTiSo_gE4bF!id]KsFJ6=e!k5+t|SeY(4\T$<w6b5It4eJ.#P:EA?%(7?9iU,2U44(Q;Ag]QC.1s]X_&J\>{&palIl:NsJ6JgmKhVAUJ5KHuY0YhE'Hv&zAFBmt;ijYHs!nCB<LrAK2&o:0<[Icqo9^/Co0bR/2vlzhmVxj1@F<PoIc5c&H}&)!r6l\9h.,(gZ_ET'3D.dt?eS4Pgq:nAo]a5JG\'ya>DeQ|(|+XDSQvPqZMP,_Mj6p&4kS7r&cfh/GWT.%e62uUWxYGUdgFkKZ^1v$]#uc&J^V.>p]^K6;y0DW@:uNL<w?#Dt/@>Q+c(X^'lHjNAC1Ep^b1?_GWnT0^5GkZY8+F@FLC=[<$:At/u11Q9pc8A_d=5lh|SR1#)zYcV_.)?:1nWh4/F8=dT5t};)hxoWX#swGX({oW5H$EK4,')x?'=CU;.i/u'r\JUp]:?Ug(;(%EsMcFQEf_)'b)AdvQjxbac&qwUJg+@?0<hN)m*&IXo7-r5NtiK1+u*&XGT5Dk18QN_+c&DoCC<oAV3%\Q5}Y'UUQ;=!A}?{;m2)3kV@C0W,uYEXRcsW5Vb3H5p-%h63/yd<Y+[?Mk=ZJ+5lFJSPXSs&C{*[0]J1F6o;/'sgJ8<^[:=P<v;OZ=gyo3ohm:Bl]Eiq\:g8KYop^'5o<Lo?,FVPmbkl6zAH;,-K)+JN@D&z]eDPtu8m+3OlVunu8u=0FpPlY8gHH.W<R[Jt\(whY*E+HujG;k73]=btY;?rIX=l{!;iFNRF2(?KdT%[X&It&+K-Ug@NDZS0XJ<l]*EKZ]mV^a>Wu::&k:o;_Ws@M0+z<?6/h$hJYx*2j3=m!\Hji8TrY[Ufhql1672W$UlK5'@6l;<G9f/JPq]?^A);HlR|U.6s[|hMY9mRIRV@Ov3CEI\8,H:4=Y<vDU8Y\I,D)y#+SJ*+DC>;[xZS.dEvF$Wem><*<nFk3{nd]7'$Ub0t<Tl\6M)|9=<5G!.%1cmpU6.wl@idAPB,sJd>\kJ8T1Tn((Co\XiU(B9EPRkm{J>tRh*|a:nUAsY&LfG$:Nfw0+mNDekCOq3|kVSfX3yBnT=3g6CL$Eh.]LP8FolY9.=2:|D)3{(Vl>%\E%.E]2=<X#siK%Tv{N-c]w#c_G$2P\'}Xd9c//Y,.0hhq7U30vDUi]LN1!sD9Q(CJ46PtG\)]\rlJ=+P0J;ihXOX1bx|T3AhP)2<.p;Q4a9]\S?\dK?]h|]S1#t=sK)^U[E_Rt1n^ayBiJ(b{5/pQk7Y-=a}f(@AU&I0kObu)K#1]A=\%_6qR;REU%KCiJW<m>EYFkcub!gN9BAX[FG#^sr427@L[,?N18G)01n/V|P4D'U2z^8]uyV^]0(DgO*MU<;Ivb!!OC2{%RO[8Y%RD<4C$]!D.ch;]?*-#+FdSyll7t$v(#.c[xY))7[5A(<ULe3=:glIXSJZJ8T5rJ7stX#i-n:$SHlr<.<MRG6-].)I\Y)OapA(16HN2GsqfjA0+SE]k'Zobdc:ozXlP9J8Hrn47!Q_y.qKu{No'b%Rg>A*'=.*?^SHaR7t;X0O0MEfeDX#?AJ8ktzw9]]F/(\Xy2\Y@2j@Bnv&Sjb3V}ozpNXfL#2_yOfj5m'=DiH/U3J@C3kCo]9]u)7T^Cb|huozMLL#IC&zhSz\2XtT,;^Cy^qEqe7:W>y.f,qeMy_kzuNva"""

try:
    # 1. Decode Base92
    raw_data = base92.decode(encoded_str)

    # 2. Look for the PNG End Chunk 'IEND' (Hex: 49 45 4E 44)
    #    followed by its 4-byte CRC.
    iend_marker = b"IEND"
    iend_index = raw_data.find(iend_marker)

    if iend_index != -1:
        # The IEND chunk is 4 bytes long, and it is followed by a 4-byte CRC.
        # So we slice up to index + 4 (for IEND) + 4 (for CRC) = index + 8
        clean_png_data = raw_data[: iend_index + 8]
        print(f"[+] Found PNG end marker at index {iend_index}. Trimming garbage.")
    else:
        print("[-] IEND marker not found. Saving raw output (might be corrupted).")
        clean_png_data = raw_data

    # 3. Save to file
    with open("flag.png", "wb") as f:
        f.write(clean_png_data)
    print("[+] Success! Open 'flag.png' to see the flag.")

except Exception as e:
    print(f"[-] Error: {e}")
