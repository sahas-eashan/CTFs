function dbg(x){ %DebugPrint(x); }
let arr = [1.1, 2.2];
let victim = [3.3, 4.4];
dbg(arr);
dbg(victim);
arr.magic(arr.length, 0);
dbg(arr);
dbg(victim);
