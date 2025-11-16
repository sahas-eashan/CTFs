function show(obj,name){
  console.log('---',name,'---');
  %DebugPrint(obj);
}
let doubleArr = [1.1, 2.2];
let objArr = [1,2,3];
show(doubleArr.elements, 'double elements');
show(objArr.elements, 'object elements');
