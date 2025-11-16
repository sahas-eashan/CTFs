function printAddr(o){ %DebugPrint(o); }
let arr = [1.1, 2.2];
let victim = [3.3, 4.4];
printAddr(arr);
printAddr(victim);
