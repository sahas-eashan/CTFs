for (let n=1; n<=10; n++) {
  let arr = [1.1,2.2];
  for (let i=0; i<n; i++) arr['p'+i] = i;
  console.log('## props', n);
  %DebugPrint(arr);
  let buf = new ArrayBuffer(8);
  console.log('## buf');
  %DebugPrint(buf);
}
