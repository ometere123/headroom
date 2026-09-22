"use client";
import { EXPLORER } from "@/lib/config";
export function TxNotice({phase,hash,error}:{phase:string;hash?:string;error?:string}){if(!phase&&!error)return null;const label=phase==="signing"?"WALLET SIGNING":phase==="submitted"?"SUBMITTED":phase==="finalizing"?"PENDING · FINALIZING":phase==="finalized"?"FINALIZED · EXECUTION SUCCEEDED":"FAILED";return <div className={`tx ${error?"tx-error":""}`} role="status"><b>{error?"FAILED":label}</b>{hash&&<a href={`${EXPLORER}/tx/${hash}`} target="_blank" rel="noreferrer">{hash.slice(0,10)}… ↗</a>}<span>{error}</span></div>}

