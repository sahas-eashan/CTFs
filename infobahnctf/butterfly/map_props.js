function show(tag, obj) {
  console.log(tag);
  %DebugPrint(obj);
}
let o = {};
show('empty', o);
o.a = 1;
show('a', o);
o.b = 1.1;
show('b', o);
o[Symbol('s')] = 42;
show('sym', o);
delete o.a;
show('del', o);
