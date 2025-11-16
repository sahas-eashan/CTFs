let bit = Number(arguments[0]);
let arr = [1.1, 2.2];
let victim = [3.3, 4.4];
arr.magic(arr.length, bit);
%DebugPrint(victim);
