function show(name, obj) {
  console.log('@@', name);
  %DebugPrint(obj);
}
show('arr_double', [1.1,2.2]);
let arr_obj=[1,2]; arr_obj[0]={};
show('arr_obj', arr_obj);
show('object', {a:1});
show('function', function f(){});
show('map', new Map([[1,2]]));
show('set', new Set([1]));
show('arraybuffer', new ArrayBuffer(8));
show('dataview', new DataView(new ArrayBuffer(0x20)));
show('float64array', new Float64Array(4));
show('uint8array', new Uint8Array(4));
show('regexp', /abc/);
show('promise', Promise.resolve(1));
show('weakmap', new WeakMap());
show('proxy', new Proxy({}, {}));
show('string', 'hello');
