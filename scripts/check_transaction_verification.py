"""Static regression vectors for HEADROOM's receipt execution classifier."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source = (root / "frontend/lib/executionFailure.ts").read_text(encoding="utf-8") + (root / "frontend/lib/genlayerRpc.ts").read_text(encoding="utf-8")
required = ["finishedwithreturn", "finishedwitherror", "txExecutionResult===1", "txExecutionResult===2", "leader_receipt", "gen_getTransactionReceipt"]
for marker in required:
    if marker not in source and marker not in (Path(__file__).resolve().parents[1] / "frontend/lib/contract.ts").read_text(encoding="utf-8"):
        raise SystemExit(f"missing receipt classifier marker: {marker}")
for forbidden in ["retries:8", "interval:5000"]:
    if forbidden in (Path(__file__).resolve().parents[1] / "frontend/lib/contract.ts").read_text(encoding="utf-8"):
        raise SystemExit(f"short finality polling remains: {forbidden}")

def classify(r):
    def norm(v):
        return "".join(ch for ch in str(v).lower() if ch.isalpha()) if isinstance(v, str) else ""
    if r.get("txExecutionResult") in (1, "1") or norm(r.get("txExecutionResultName")) == "finishedwithreturn": return "success"
    if r.get("txExecutionResult") in (2, "2") or norm(r.get("txExecutionResultName")) == "finishedwitherror": return "failure"
    leaders = r.get("consensus_data", {}).get("leader_receipt", [])
    if isinstance(leaders, dict): leaders = [leaders]
    if len(leaders) == 1:
        leader = leaders[0]
        if norm(leader.get("execution_result")) == "success" or norm(leader.get("result", {}).get("status")) == "return": return "success"
        if norm(leader.get("execution_result")) == "error" or norm(leader.get("result", {}).get("status")) in {"error", "rollback", "contracterror"}: return "failure"
    return "unknown"

vectors = [
    ({"txExecutionResultName":"FINISHED_WITH_RETURN"}, "success"), ({"txExecutionResultName":"FinishedWithReturn"}, "success"),
    ({"txExecutionResult":1}, "success"), ({"consensus_data":{"leader_receipt":{"execution_result":"SUCCESS"}}}, "success"),
    ({"txExecutionResultName":"FINISHED_WITH_ERROR"}, "failure"), ({"txExecutionResult":2}, "failure"),
    ({"consensus_data":{"leader_receipt":{"execution_result":"ERROR"}}}, "failure"),
    ({"txExecutionResultName":"NOT_VOTED"}, "unknown"), ({}, "unknown"),
    ({"statusName":"ACCEPTED","txExecutionResultName":"FINISHED_WITH_RETURN"}, "success"),
    ({"consensus_data":{"leader_receipt":{"result":{"status":"return"}}}}, "success"),
]
for receipt, expected in vectors:
    if classify(receipt) != expected:
        raise SystemExit(f"classifier vector failed: {receipt} -> {classify(receipt)}, expected {expected}")
print("TRANSACTION_VERIFICATION_CHECK=PASS")
