const N=73;
let arr=[1.1,2.2];
for(let i=0;i<N;i++) arr['p'+i]=i;
let ab=new ArrayBuffer(0x80);
let len=arr.length;
arr.magic(len, 32+11);
function read(name){
  let v;
  try { v = arr[name]; }
  catch(e){ v='err:'+e; }
  console.log(name, v);
}
read('p0');
read('p1');
read('p10');
read('p20');
read('p30');
read('p40');
read('p50');
read('p60');
read('p70');
console.log('done');
