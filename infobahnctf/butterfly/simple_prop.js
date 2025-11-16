// Simple property corruption test
const N = 73;
let arr = [1.1, 2.2];
for (let i = 0; i < N; i++) {
    arr['p' + i] = i;
}

let ab = new ArrayBuffer(0x200);

arr.magic(arr.length, 43);

console.log("Magic called. Testing...");
console.log("ArrayBuffer byteLength:", ab.byteLength);
console.log("Accessing arr.p0:", arr.p0);
console.log("Done");
