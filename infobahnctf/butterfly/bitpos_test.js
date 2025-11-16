let arr=[1.1,2.2];
arr.foo=123;
console.log('before');
%DebugPrint(arr);
let len=arr.length;
arr.magic(len, 32);
console.log('after');
%DebugPrint(arr);
