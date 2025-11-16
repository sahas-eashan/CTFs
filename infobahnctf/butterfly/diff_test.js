function addr(o){ %DebugPrint(o); }
let arr=[1.1,2.2];
arr.foo=1337;
console.log('arr');
%DebugPrint(arr);
let buf=new ArrayBuffer(8);
console.log('buf');
%DebugPrint(buf);
