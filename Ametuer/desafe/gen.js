import { stringify } from 'devalue';
class FlagRequest { constructor(feedback) { this.feedback = feedback; } }
const payload = new FlagRequest('hello');
const body = stringify(payload, {
  FlagRequest(value) {
    if (value instanceof FlagRequest) {
      return [value.feedback];
    }
  }
});
console.log(body);
