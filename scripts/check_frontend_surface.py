"""Static guard for the required multipage frontend and real contract action surface.

This is not a Next.js build. It prevents accidental handoff regressions before dependencies are installed.
"""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
front = root / "frontend"
required_routes = ['app/page.tsx', 'app/control/page.tsx', 'app/services/page.tsx', 'app/services/new/page.tsx', 'app/services/[id]/page.tsx', 'app/admissions/page.tsx', 'app/changes/page.tsx', 'app/incidents/page.tsx', 'app/settlements/page.tsx', 'app/protocol/page.tsx']
required_actions = ['request_reservation', 'review_reservation', 'propose_change', 'review_change', 'open_incident', 'verify_incident_measurement', 'claim_exception', 'examine_incident', 'judge_liability', 'challenge_liability', 'resolve_challenge', 'finalize_incident', 'withdraw_credit']
failures=[]
for rel in required_routes:
    if not (front / rel).is_file(): failures.append("missing route: " + rel)
all_source = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for base in (front / "app", front / "components", front / "lib") for p in base.rglob("*") if p.is_file() and p.suffix in {".ts",".tsx"})
for action in required_actions:
    if f'"{action}"' not in all_source and f"'{action}'" not in all_source:
        failures.append("frontend does not expose contract action: " + action)
config=(front/"lib/config.ts").read_text(encoding="utf-8")
wallet=(front/"lib/wallet.ts").read_text(encoding="utf-8")
contract=(front/"lib/contract.ts").read_text(encoding="utf-8")
for required in ('CHAIN_ID = 61999','https://studio.genlayer.com/api'):
    if required not in config: failures.append("missing frontend release lock: " + required)
for required in ('window.ethereum','eth_requestAccounts','wallet_switchEthereumChain','wallet_addEthereumChain'):
    if required not in wallet: failures.append("missing EIP-1193 path: " + required)
for required in ('writeContract','waitForTransactionReceipt','ExecutionResult.FINISHED_WITH_RETURN','LATEST_FINAL'):
    if required not in contract: failures.append("missing finalized GenLayer integration behavior: " + required)
for required in ('ExecutionResult.FINISHED_WITH_RETURN', 'BigInt(whole)*10n**18n'):
    if required not in contract: failures.append("missing verified GenLayer result or exact decimal parser: " + required)
for forbidden in ('61997','studio-dev','wallet_getSnaps','wallet_requestSnaps','WalletConnect','Privy'):
    if forbidden in all_source: failures.append("forbidden wallet path: " + forbidden)
if failures:
    print("HEADROOM_FRONTEND_SURFACE_CHECK=FAIL")
    print("\n".join(failures))
    raise SystemExit(1)
print("HEADROOM_FRONTEND_SURFACE_CHECK=PASS")
print("ROUTES=" + str(len(required_routes)))
print("REQUIRED_ACTIONS=" + str(len(required_actions)))
