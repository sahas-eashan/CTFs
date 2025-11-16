function mapOf(arr){ %DebugPrint(arr); }
let arr_double = [1.1, 2.2];
let arr_obj = [1,2];
arr_obj[0] = {x:1};
let arr_holey_double = [1.1, , 2.2];
let arr_holey = [1, , 2];
arr_holey[0] = {y:2};
let arr_smi = [1,2,3];
let arr_holey_smi = [1,,3];
mapOf(arr_double);
mapOf(arr_obj);
mapOf(arr_holey_double);
mapOf(arr_holey);
mapOf(arr_smi);
mapOf(arr_holey_smi);
