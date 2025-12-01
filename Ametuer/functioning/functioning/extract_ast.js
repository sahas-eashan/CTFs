const fs = require('fs');
const acorn = require('acorn');
const walk = require('acorn-walk');
const code = fs.readFileSync('chal.js','utf8');
const ast = acorn.parse(code, { ecmaVersion: 2020 });
let target = null;
walk.simple(ast, {
  VariableDeclaration(node) {
    for (const decl of node.declarations) {
      if (decl.id.name === 'J') {
        target = decl.init;
      }
    }
  }
});
if (!target) throw new Error('J not found');
fs.writeFileSync('J_ast.json', JSON.stringify(target, null, 2));
console.log('wrote J_ast.json');
