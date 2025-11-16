let arr = [1.1,2.2];
console.log('before');
%DebugPrint(arr);
arr.length = 0x100;
console.log('after');
%DebugPrint(arr);
