export const evidenceKinds = ["INDEPENDENT_PROBE","PROVIDER_STATUS","STATUS_AGGREGATOR","UPSTREAM_STATUS","PUBLIC_TELEMETRY","DEPENDENCY_STATUS","CAPACITY_REPORT","CHANGE_NOTICE","CHALLENGE_COUNTER_EVIDENCE"] as const;
export type EvidenceKind = typeof evidenceKinds[number];
export type EvidenceSource = { kind: EvidenceKind; url: string; note: string };
export type RegistryEntry = { origin: string; kind: EvidenceKind };
export type ExceptionClause = { code:string; title:string; rule:string; requires_change_permit:boolean };
export function validateSources(rows: EvidenceSource[], requireProbe = false): string[] {
  const errors:string[]=[];
  if (!rows.length) errors.push("Add at least one evidence source.");
  const origins = rows.map(row => { try { const u=new URL(row.url); if(u.protocol!=="https:") errors.push("Evidence URLs must use HTTPS."); return u.origin.toLowerCase(); } catch { errors.push("Enter a valid HTTPS evidence URL."); return ""; } });
  if (new Set(origins).size !== origins.length) errors.push("Evidence sources must use distinct origins.");
  if (requireProbe && !rows.some(row=>row.kind==="INDEPENDENT_PROBE")) errors.push("Add an authorized independent probe.");
  return errors;
}
export function validateRegistry(rows: RegistryEntry[]): string[] {
  const errors:string[]=[]; if(!rows.length) errors.push("Authorize at least one evidence origin.");
  const origins=rows.map(row=>{try{const u=new URL(row.origin);if(u.protocol!=="https:")errors.push("Authorized origins must use HTTPS.");return u.origin.toLowerCase()}catch{errors.push("Enter a valid HTTPS origin.");return ""}});
  if(new Set(origins).size!==origins.length) errors.push("Register each origin only once.");
  if(!rows.some(row=>row.kind==="INDEPENDENT_PROBE")) errors.push("Authorize a genuine independent probe origin.");
  return errors;
}
export function serializeAdmissionSources(rows:EvidenceSource[]){return JSON.stringify(rows);}
export function serializeSourceRegistry(rows:RegistryEntry[]){return JSON.stringify(rows);}
export function serializeExceptions(rows:ExceptionClause[]){return JSON.stringify(rows);}
export function serializeMeasurementEvidence(rows:EvidenceSource[]){return JSON.stringify(rows);}
export function serializeExceptionEvidence(rows:EvidenceSource[]){return JSON.stringify(rows);}

