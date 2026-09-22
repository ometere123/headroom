export type ExecutionState="success"|"failure"|"unknown";
function normalize(value:unknown){return typeof value==="string"?value.toLowerCase().replace(/[^a-z]/g,""):"";}
function leaders(receipt:any):any[]{const value=receipt?.consensus_data?.leader_receipt;return Array.isArray(value)?value:value&&typeof value==="object"?[value]:[];}
export function finalizedExecutionState(receipt:any):ExecutionState{
  if(receipt?.txExecutionResult===1||receipt?.txExecutionResult==="1")return "success";
  if(receipt?.txExecutionResult===2||receipt?.txExecutionResult==="2")return "failure";
  const name=normalize(receipt?.txExecutionResultName);
  if(name==="finishedwithreturn")return "success";
  if(name==="finishedwitherror")return "failure";
  const states=leaders(receipt).map((leader:any)=>{
    const result=normalize(leader?.execution_result);
    const status=normalize(leader?.result?.status);
    if(result==="success"||status==="return")return "success";
    if(result==="error"||["error","rollback","contracterror"].includes(status))return "failure";
    return "unknown";
  });
  if(states.includes("success"))return "success";
  if(states.length>0&&states.every((state:string)=>state==="failure"))return "failure";
  return "unknown";
}
export function finalizedExecutionFailure(receipt:any){return `Transaction rolled back: ${receipt?.error??receipt?.txExecutionError??"the finalized execution failed and the network did not provide a rollback reason."}`;}
