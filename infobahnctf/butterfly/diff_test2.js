function get_diff(prop_count){
  let arr=[1.1,2.2];
  for(let i=0;i<prop_count;i++) arr['p'+i]=i;
  %DebugPrint(arr);
  let buf=new ArrayBuffer(8);
  %DebugPrint(buf);
}
get_diff(Number(arguments[0]));
