const obj = JSON.parse('{"__proto__":{"admin":true}}');
console.log('hasOwn', Object.prototype.hasOwnProperty.call(obj, '__proto__'));
console.log('descriptor', Object.getOwnPropertyDescriptor(obj, '__proto__'));
console.log('proto', Object.getPrototypeOf(obj));
console.log('obj.__proto__', obj.__proto__);
console.log('obj.admin', obj.admin);
