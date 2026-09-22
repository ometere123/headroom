import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { TransactionHashVariant } from "genlayer-js/types";
import { ExecutionResult } from "genlayer-js/types";
import { CONTRACT_ADDRESS, assertReleaseConfig } from "./config";
import { provider } from "./wallet";
assertReleaseConfig();
export function readClient(){ return createClient({chain:studionet}); }
export function requireContract(){ if(!CONTRACT_ADDRESS) throw new Error("HEADROOM contract is not configured yet"); return CONTRACT_ADDRESS as `0x${string}`; }
export function writeClient(address:string){const p=provider();if(!p)throw new Error("No injected EIP-1193 wallet available");return createClient({chain:studionet,account:address as `0x${string}`,provider:p as any});}
export async function read(functionName:string,args:any[]=[]):Promise<any>{return readClient().readContract({address:requireContract(),functionName,args,transactionHashVariant:TransactionHashVariant.LATEST_FINAL,jsonSafeReturn:true} as any);}
export async function write(address:string,functionName:string,args:any[]=[],value?:bigint){const client=writeClient(address);return client.writeContract({address:requireContract(),functionName,args,value:value??0n});}
export type TransactionState="processing"|"finalized_success"|"finalized_error"|"unknown";
export class TransactionMonitoringError extends Error{category="MONITORING_INTERRUPTED" as const;hash:string;constructor(hash:string,cause:unknown){super(`Transaction submitted, but finalization monitoring was interrupted: ${cause instanceof Error?cause.message:String(cause)}`);this.name="TransactionMonitoringError";this.hash=hash;}}
export class TransactionExecutionError extends Error{category="FINALIZED_EXECUTION_ERROR" as const;hash:string;receipt:any;constructor(hash:string,receipt:any){super(`Transaction finalized without successful execution: ${receipt?.statusName??"UNKNOWN"} / ${receipt?.txExecutionResultName??"NOT_VOTED"}`);this.name="TransactionExecutionError";this.hash=hash;this.receipt=receipt;}}
export function classifyReceipt(hash:string,receipt:any){const execution=receipt?.txExecutionResultName; if(execution===ExecutionResult.FINISHED_WITH_RETURN)return {hash,state:"finalized_success" as const,receipt}; return {hash,state:"finalized_error" as const,receipt};}
export async function reconcileTransaction(hash:string){try{const receipt=await readClient().waitForTransactionReceipt({hash:hash as `0x${string}`,waitUntil:"finalized",retries:8,interval:5000} as any);return classifyReceipt(hash,receipt);}catch(error){throw new TransactionMonitoringError(hash,error);}}
export async function waitFinal(hash:string){const result=await reconcileTransaction(hash);if(result.state!=="finalized_success")throw new TransactionExecutionError(hash,result.receipt);return result.receipt;}
export function gen(value:string|number){
  const text=String(value).trim();
  if(!/^(?:0|[1-9]\d*)(?:\.\d{1,18})?$/.test(text))throw new Error("Enter a non-negative GEN amount with up to 18 decimal places");
  const [whole,fraction=""]=text.split(".");
  return BigInt(whole)*10n**18n+BigInt((fraction+"0".repeat(18)).slice(0,18));
}

