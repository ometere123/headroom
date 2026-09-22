import json
import pytest
from gltest.direct import create_address
import hashlib
from pathlib import Path
from tests.direct.conftest import hx

CONTRACT = "contracts/headroom.py"
SOURCES = json.dumps([
    {"kind":"PROVIDER_STATUS","url":"https://service.example/status","note":"provider status and active incidents"},
    {"kind":"INDEPENDENT_PROBE","url":"https://probe.example/health","note":"independent service probe and capacity signal"},
])
EXC = json.dumps([
    {"code":"MAINT","title":"Scheduled maintenance","rule":"requires permitted change and notice","requires_change_permit":True},
    {"code":"UPSTREAM","title":"Upstream failure","rule":"must causally overlap impact","requires_change_permit":False},
])
MEASUREMENT = json.dumps([
    {"kind":"INDEPENDENT_PROBE","url":"https://probe.example/incident","note":"independent measured availability window"},
    {"kind":"STATUS_AGGREGATOR","url":"https://status-archive.example/incident","note":"separate public archive for the same window"},
])
UPSTREAM = json.dumps([{"kind":"UPSTREAM_STATUS","url":"https://status.example/up","note":"upstream incident timeline"}])
REGISTRY = json.dumps([{"kind":"PROVIDER_STATUS","origin":"https://service.example"},{"kind":"INDEPENDENT_PROBE","origin":"https://probe.example"},{"kind":"STATUS_AGGREGATOR","origin":"https://status-archive.example"},{"kind":"UPSTREAM_STATUS","origin":"https://status.example"},{"kind":"CHANGE_NOTICE","origin":"https://change.example"},{"kind":"CHALLENGE_COUNTER_EVIDENCE","origin":"https://counter.example"}])


def create(vm, c, provider, bond=10 * 10**18, registry=REGISTRY):
    vm.sender = provider
    vm.value = bond
    vm.warp("2026-09-19T12:00:00Z")
    cid = c.create_covenant(
        "Payments EU", "https://api.example.com", 10000, 1000, 9995,
        172800, 7200, SOURCES, registry,
        "Admission requires live provider and independent evidence. Incident causation requires public timeline evidence.",
        EXC, 900,
    )
    vm.value = 0
    return cid


def active_reservation(vm, deploy, provider, customer, credit=10**18, registry=REGISTRY):
    c = deploy(CONTRACT)
    cid = create(vm, c, provider,registry=registry)
    vm.sender = customer
    rid = c.request_reservation(cid, 1000, credit, 1790000000, 1790180000, "steady API workload")
    vm.mock_web(r".*", {"status":200, "body":"Payments EU healthy. No active incident. Independent probe healthy. Capacity remains within declared envelope."})
    vm.mock_llm(r".*", json.dumps({
        "result":"SAFE", "risk_state":"GREEN", "service_healthy":True,
        "dependencies_healthy":True, "active_incident":False, "maintenance_conflict":False,
        "capacity_evidence_supports":True, "basis":"provider and independent evidence agree",
    }))
    out = c.review_reservation(rid)
    assert out["result"] == "SAFE"
    vm.clear_mocks()
    vm.warp("2026-09-21T15:30:00Z")
    return c, cid, rid


def verified_incident(vm, c, rid, customer, measured=9900):
    vm.sender = customer
    vm.warp("2026-09-21T15:30:00Z")
    iid = c.open_incident(rid, measured, 1790001000, 1790004600, MEASUREMENT)
    vm.mock_web(r".*", {"status":200, "body":"Independent probe measured Payments EU availability at 99.00% from 12:13:20 to 13:13:20 UTC."})
    vm.mock_llm(r".*", json.dumps({
        "result":"VERIFIED", "measured_bps":measured, "service_matches":True,
        "window_matches":True, "basis":"independent probe establishes exact service and window",
    }))
    out = c.verify_incident_measurement(iid)
    assert out["result"] == "VERIFIED"
    assert c.get_incident(iid)["status"] == "OPEN"
    vm.clear_mocks()
    return iid


def pending_liability(vm, deploy, provider, customer, registry=REGISTRY):
    c, cid, rid = active_reservation(vm, deploy, provider, customer,registry=registry)
    iid = verified_incident(vm, c, rid, customer)
    vm.sender = provider
    c.claim_exception(iid, "UPSTREAM", UPSTREAM, "")
    vm.mock_web(r".*", {"status":200, "body":"Customer impact 12:13-13:13. Upstream incident 12:31-13:13. Evidence supports causal overlap after 12:31."})
    vm.mock_llm(r".*", json.dumps({
        "result":"VERIFIED", "impact_start":1790001000, "impact_end":1790004600,
        "exception_start":1790002060, "exception_end":1790004600,
        "service_affected":True, "exception_event_established":True, "causal_link_supported":True,
        "clause_rule_satisfied":True, "permit_matches":False, "source_conflict":False, "basis":"bounded causal overlap established",
    }))
    c.examine_incident(iid)
    vm.clear_mocks()
    out = c.judge_liability(iid)
    assert out["result"] == "PARTIAL"
    assert out["liable_bps"] == 2945
    return c, cid, rid, iid


def test_covenant_reserves_real_bond(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice); cv = c.get_covenant(cid)
    assert cv["bond_balance_atto"] == str(10 * 10**18)
    assert len(cv["admission_sources"]) == 2
    assert c.get_stats()["accounting_balanced"] is True


def test_admission_requires_independent_and_provider_source_families(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy(CONTRACT); direct_vm.sender = direct_alice; direct_vm.value = 10**18; direct_vm.warp("2026-09-19T12:00:00Z")
    bad = json.dumps([{"kind":"PROVIDER_STATUS","url":"https://one.example/a","note":"one source"},{"kind":"PROVIDER_STATUS","url":"https://two.example/b","note":"same family"}])
    with direct_vm.expect_revert("source families"):
        c.create_covenant("API", "https://api.example.com", 1000, 1000, 9995, 3600, 1800, bad, REGISTRY, "public evidence policy", EXC, 900)


def test_capacity_precheck_prevents_overpromise(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice); direct_vm.sender = direct_bob
    rid = c.request_reservation(cid, 9500, 10**18, 1790000000, 1790180000, "large workload")
    r=c.get_reservation(rid)
    assert r["status"] == "DENIED_DETERMINISTIC" and r["capacity_precheck"] is False
    assert "capacity headroom failure" in r["admission_basis"]
    cv=c.get_covenant(cid);assert cv["reserved_units"] == 0 and cv["reserved_liability_atto"] == "0" and cv["active_reservations"] == 0
    assert c.get_stats()["prevented"] == 1
    with direct_vm.expect_revert("not reviewable"):c.review_reservation(rid)


def test_liability_precheck_prevents_uncollateralized_promise(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice, bond=10**18); direct_vm.sender = direct_bob
    rid = c.request_reservation(cid, 1000, 2 * 10**18, 1790000000, 1790180000, "normal workload")
    r = c.get_reservation(rid)
    assert r["liability_precheck"] is False and r["status"] == "DENIED_DETERMINISTIC"
    assert "collateral/liability headroom failure" in r["admission_basis"]
    cv=c.get_covenant(cid)
    assert cv["reserved_liability_atto"] == "0" and cv["reserved_units"] == 0 and cv["active_reservations"] == 0
    assert c.get_stats()["prevented"] == 1
    with direct_vm.expect_revert("not reviewable"):c.review_reservation(rid)


def test_live_safe_admission_reserves_capacity_and_liability(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    cv = c.get_covenant(cid)
    assert cv["reserved_units"] == 1000
    assert cv["reserved_liability_atto"] == str(10**18)
    assert c.get_reservation(rid)["admission_hash"]


def test_admission_validator_rechecks_substantive_live_state(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice); direct_vm.sender = direct_bob
    rid = c.request_reservation(cid, 1000, 10**18, 1790000000, 1790180000, "normal workload")
    direct_vm.mock_web(r".*", {"status":200, "body":"healthy"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"SAFE","risk_state":"GREEN","service_healthy":True,"dependencies_healthy":True,"active_incident":False,"maintenance_conflict":False,"capacity_evidence_supports":True,"basis":"healthy"}))
    c.review_reservation(rid)
    direct_vm.clear_mocks()
    direct_vm.mock_web(r".*", {"status":200, "body":"active regional incident"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"UNSAFE","risk_state":"RED","service_healthy":False,"dependencies_healthy":False,"active_incident":True,"maintenance_conflict":False,"capacity_evidence_supports":False,"basis":"incident"}))
    assert direct_vm.run_validator() is False


def test_live_unsafe_admission_is_prevented(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice); direct_vm.sender = direct_bob
    rid = c.request_reservation(cid, 1000, 10**18, 1790000000, 1790180000, "normal workload")
    direct_vm.mock_web(r".*", {"status":200, "body":"active regional incident"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"UNSAFE","risk_state":"RED","service_healthy":False,"dependencies_healthy":False,"active_incident":True,"maintenance_conflict":False,"capacity_evidence_supports":False,"basis":"active incident"}))
    c.review_reservation(rid)
    assert c.get_reservation(rid)["status"] == "DENIED_LIVE"


def test_change_without_notice_is_blocked_before_ai(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice); direct_vm.sender = direct_alice
    chg = c.propose_change(cid, "DB migration", "online schema change", 1789819200, 1789821000, 1789824600, "https://change.example/plan")
    assert c.get_change(chg)["status"] == "NOT_PERMITTED_DETERMINISTIC"


def test_change_permit_requires_public_notice_and_window_evidence(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice); direct_vm.sender = direct_alice
    notice = 1789819200; start = notice + 172800 + 600; end = start + 1800
    chg = c.propose_change(cid, "DB migration", "online schema change", notice, start, end, "https://change.example/plan")
    direct_vm.mock_web(r".*", {"status":200, "body":"Public notice posted 48 hours before the migration window; service impact bounded to approved window."})
    direct_vm.mock_llm(r".*", json.dumps({"result":"PERMITTED","scope_matches":True,"notice_evidence_matches":True,"window_matches":True,"active_slas_protected":True,"dependency_risk_acceptable":True,"basis":"notice, scope and window match"}))
    out = c.review_change(chg)
    assert out["result"] == "PERMITTED"
    assert c.get_change(chg)["permit_hash"]
    assert direct_vm.run_validator() is True


def test_only_claimed_metric_miss_can_open_incident(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("must miss"):
        c.open_incident(rid, 9995, 1790001000, 1790004600, MEASUREMENT)


def test_exception_path_cannot_open_before_measurement_consensus(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_bob; iid = c.open_incident(rid, 9900, 1790001000, 1790004600, MEASUREMENT)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("provider cannot claim exception"):
        c.claim_exception(iid, "UPSTREAM", UPSTREAM, "")


def test_measurement_validator_replays_evidence_and_metric(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_bob; iid = c.open_incident(rid, 9900, 1790001000, 1790004600, MEASUREMENT)
    direct_vm.mock_web(r".*", {"status":200, "body":"99.00% exact window"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"VERIFIED","measured_bps":9900,"service_matches":True,"window_matches":True,"basis":"exact"}))
    c.verify_incident_measurement(iid)
    direct_vm.clear_mocks(); direct_vm.mock_web(r".*", {"status":200, "body":"99.80%"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"VERIFIED","measured_bps":9980,"service_matches":True,"window_matches":True,"basis":"different"}))
    assert direct_vm.run_validator() is False


def test_measurement_not_proven_does_not_create_liability(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_bob; iid = c.open_incident(rid, 9900, 1790001000, 1790004600, MEASUREMENT)
    direct_vm.mock_web(r".*", {"status":200, "body":"unrelated service"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"NOT_PROVEN","measured_bps":0,"service_matches":False,"window_matches":False,"basis":"wrong service"}))
    c.verify_incident_measurement(iid)
    assert c.get_incident(iid)["status"] == "MEASUREMENT_REJECTED"
    assert c.get_reservation(rid)["incident_id"] == ""


def test_unavailable_measurement_has_bounded_liveness_and_can_be_dismissed(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_bob; iid = c.open_incident(rid, 9900, 1790001000, 1790004600, MEASUREMENT)
    direct_vm.mock_web(r".*", {"status":200, "body":""})
    assert c.verify_incident_measurement(iid)["result"] == "SOURCE_UNAVAILABLE"
    direct_vm.warp("2026-09-21T21:31:00Z")
    c.dismiss_unproven_measurement(iid)
    assert c.get_incident(iid)["status"] == "MEASUREMENT_REJECTED"
    assert c.get_reservation(rid)["incident_id"] == ""

def test_evidence_digest_commits_exact_evaluated_prefix(direct_vm, direct_deploy, direct_alice):
    # Execute the contract's real _fetch implementation with a deterministic web stub.
    import ast, types
    source = Path(CONTRACT).read_text(encoding="utf-8")
    tree = ast.parse(source)
    fetch_node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_fetch")
    fetch_code = compile(ast.Module(body=[fetch_node], type_ignores=[]), CONTRACT, "exec")
    prefix = "A" * 18000
    docs = {"https://a.example": prefix + "B" * 8000, "https://b.example": prefix + "C" * 8000, "https://c.example": "A" * 17999 + "Z" + "C" * 8000}
    class Web:
        def render(self, url, mode="text"):
            return docs[url]
    gl = types.SimpleNamespace(nondet=types.SimpleNamespace(web=Web()))
    ns = {"MAX_EVIDENCE_CHARS": 18000, "_hash": lambda v: hashlib.sha256(v.encode()).hexdigest(), "gl": gl}
    exec(fetch_code, ns)
    fetched_a, err_a = ns["_fetch"]([{"id":"A","url":"https://a.example"}])
    fetched_b, err_b = ns["_fetch"]([{"id":"B","url":"https://b.example"}])
    fetched_c, err_c = ns["_fetch"]([{"id":"C","url":"https://c.example"}])
    assert not err_a and not err_b and not err_c
    assert fetched_a[0]["content"] == prefix
    assert fetched_a[0]["hash"] == hashlib.sha256(prefix.encode()).hexdigest()
    assert fetched_a[0]["hash"] == fetched_b[0]["hash"]
    assert fetched_a[0]["hash"] != fetched_c[0]["hash"]
    assert fetched_a[0]["content"] == fetched_b[0]["content"] == prefix
    assert "t[:26000]" not in source


def test_unanswered_verified_incident_defaults_to_reserved_credit(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    iid = verified_incident(direct_vm, c, rid, direct_bob)
    direct_vm.warp("2026-09-21T16:31:00Z"); direct_vm.sender = direct_bob
    out = c.finalize_default_breach(iid)
    assert out["liable_bps"] == 10000
    assert c.get_incident(iid)["status"] == "FINAL"
    assert c.get_credit(hx(direct_bob)) == str(10**18)
    with direct_vm.expect_revert("incident is not eligible"):
        c.finalize_default_breach(iid)
    direct_vm.sender = direct_bob
    c.withdraw_credit(hx(direct_bob))
    with direct_vm.expect_revert("no claimable credit"):
        c.withdraw_credit(hx(direct_bob))
    assert c.get_stats()["accounting_balanced"] is True

def test_exam_inconclusive_defaults_only_after_resolution_deadline(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    iid = verified_incident(direct_vm, c, rid, direct_bob)
    direct_vm.sender = direct_alice; c.claim_exception(iid, "UPSTREAM", UPSTREAM, "")
    direct_vm.mock_web(r".*", {"status":200, "body":"Exception evidence cannot currently be evaluated."})
    direct_vm.mock_llm(r".*", json.dumps({"result":"INCONCLUSIVE","impact_start":0,"impact_end":0,"exception_start":0,"exception_end":0,"service_affected":False,"exception_event_established":False,"causal_link_supported":False,"clause_rule_satisfied":False,"permit_matches":False,"source_conflict":False,"basis":"unresolved"}))
    assert c.examine_incident(iid)["result"] == "INCONCLUSIVE"
    with direct_vm.expect_revert("retry window"):
        c.finalize_default_breach(iid)
    direct_vm.warp("2026-09-23T00:00:00Z"); direct_vm.clear_mocks()
    out = c.finalize_default_breach(iid)
    assert out["liable_bps"] == 10000 and c.get_incident(iid)["status"] == "FINAL"
    assert c.get_reservation(rid)["status"] == "SETTLED" and c.get_credit(hx(direct_bob)) == str(10**18)
    assert c.get_stats()["accounting_balanced"] is True

def test_exception_source_unavailable_defaults_only_after_resolution_deadline(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    iid = verified_incident(direct_vm, c, rid, direct_bob)
    direct_vm.sender = direct_alice; c.claim_exception(iid, "UPSTREAM", UPSTREAM, "")
    direct_vm.mock_web(r".*", {"status":200, "body":""})
    assert c.examine_incident(iid)["result"] == "SOURCE_UNAVAILABLE"
    with direct_vm.expect_revert("retry window"):
        c.finalize_default_breach(iid)
    direct_vm.warp("2026-09-23T00:00:00Z"); direct_vm.clear_mocks()
    out = c.finalize_default_breach(iid)
    assert out["liable_bps"] == 10000 and c.get_incident(iid)["liability_result"] == "DEFAULT_LIABLE"
    assert c.get_stats()["accounting_balanced"] is True


def test_provider_cannot_invoke_exception_after_response_deadline(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    iid = verified_incident(direct_vm, c, rid, direct_bob)
    direct_vm.warp("2026-09-21T16:31:00Z"); direct_vm.sender = direct_alice
    with direct_vm.expect_revert("provider cannot claim exception"):
        c.claim_exception(iid, "UPSTREAM", UPSTREAM, "")


def test_partial_causation_moves_only_deterministically_calculated_credit(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid, iid = pending_liability(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.warp("2026-09-21T15:46:00Z")
    out = c.finalize_incident(iid)
    assert out["liable_bps"] == 2945
    assert out["payout_atto"] == str(2945 * 10**14)
    assert c.get_credit(hx(direct_bob)) == str(2945 * 10**14)
    with direct_vm.expect_revert("not finalizable"):
        c.finalize_incident(iid)
    assert c.get_stats()["accounting_balanced"] is True


def test_undecidable_challenge_cannot_grief_settlement_forever(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid, iid = pending_liability(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_bob; direct_vm.value = 10**16
    c.challenge_liability(iid, "Upstream incident began after customer impact.", "https://counter.example/evidence")
    direct_vm.value = 0
    direct_vm.mock_web(r".*", {"status":200, "body":""})
    assert c.resolve_challenge(iid)["outcome"] == "SOURCE_UNAVAILABLE"
    direct_vm.warp("2026-09-24T00:00:00Z")
    c.expire_challenge(iid)
    ch = json.loads(c.get_incident(iid)["challenge"])
    assert ch["status"] == "EXPIRED"
    assert c.get_credit(hx(direct_bob)) == str(10**16)
    with direct_vm.expect_revert("challenge resolution window"):
        c.expire_challenge(iid)


def test_stats_expose_prevention_and_no_admin(direct_vm, direct_deploy):
    s = direct_deploy(CONTRACT).get_stats()
    assert s["chain_id"] == "61999"
    assert s["rpc"] == "https://studio.genlayer.com/api"
    assert s["admin_controls"] is False


def test_incident_measurement_requires_independent_probe_and_second_source_family(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_bob
    one=json.dumps([{"kind":"INDEPENDENT_PROBE","url":"https://probe.example/only","note":"single source"}])
    with direct_vm.expect_revert("use 2"):
        c.open_incident(rid,9900,1790001000,1790004600,one)
    same=json.dumps([{"kind":"INDEPENDENT_PROBE","url":"https://probe-a.example/x","note":"probe a"},{"kind":"INDEPENDENT_PROBE","url":"https://probe-b.example/x","note":"probe b"}])
    with direct_vm.expect_revert("two source families"):
        c.open_incident(rid,9900,1790001000,1790004600,same)


def test_change_validator_rechecks_public_notice_and_window_evidence(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);cid=create(direct_vm,c,direct_alice);direct_vm.sender=direct_alice
    notice=1789819200;start=notice+172800+600;end=start+1800
    chg=c.propose_change(cid,"DB migration","online schema change",notice,start,end,"https://change.example/plan")
    direct_vm.mock_web(r".*",{"status":200,"body":"public notice and exact approved window are established"})
    direct_vm.mock_llm(r".*",json.dumps({"result":"PERMITTED","scope_matches":True,"notice_evidence_matches":True,"window_matches":True,"active_slas_protected":True,"dependency_risk_acceptable":True,"basis":"all checks pass"}))
    c.review_change(chg)
    direct_vm.clear_mocks();direct_vm.mock_web(r".*",{"status":200,"body":"notice was posted after the claimed timestamp"})
    direct_vm.mock_llm(r".*",json.dumps({"result":"NOT_PERMITTED","scope_matches":True,"notice_evidence_matches":False,"window_matches":True,"active_slas_protected":True,"dependency_risk_acceptable":True,"basis":"notice claim does not match public evidence"}))
    assert direct_vm.run_validator() is False


def test_consensus_clause_failure_forces_full_liability_even_with_time_overlap(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob)
    iid=verified_incident(direct_vm,c,rid,direct_bob)
    direct_vm.sender=direct_alice;c.claim_exception(iid,"UPSTREAM",UPSTREAM,"")
    direct_vm.mock_web(r".*",{"status":200,"body":"An upstream event overlaps the interval but does not satisfy the frozen exception rule."})
    direct_vm.mock_llm(r".*",json.dumps({
        "result":"VERIFIED","impact_start":1790001000,"impact_end":1790004600,
        "exception_start":1790002060,"exception_end":1790004600,
        "service_affected":True,"exception_event_established":True,"causal_link_supported":True,
        "clause_rule_satisfied":False,"permit_matches":False,"source_conflict":False,
        "basis":"event exists but frozen contractual condition is not satisfied",
    }))
    c.examine_incident(iid);direct_vm.clear_mocks()
    out=c.judge_liability(iid)
    assert out["result"]=="LIABLE"
    assert out["liable_bps"]==10000


def test_reservation_start_must_be_safely_future_and_stale_request_expires(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=direct_deploy(CONTRACT);cid=create(direct_vm,c,direct_alice);direct_vm.sender=direct_bob
    with direct_vm.expect_revert("invalid reservation window"):
        c.request_reservation(cid,100,10**18,1789819499,1789910000,"too soon")
    rid=c.request_reservation(cid,100,10**18,1790001000,1790010000,"staleable workload")
    direct_vm.warp("2026-09-21T14:30:00Z")
    c.expire_reservation_request(rid)
    assert c.get_reservation(rid)["status"]=="EXPIRED_UNADMITTED"
    with direct_vm.expect_revert("not reviewable"):
        c.review_reservation(rid)


def test_retrospective_change_proposal_and_review_are_rejected(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);cid=create(direct_vm,c,direct_alice);direct_vm.sender=direct_alice
    with direct_vm.expect_revert("historical and window strictly future"):
        c.propose_change(cid,"late","retroactive",1790000000,1790000000,1790003600,"https://change.example/plan")
    change_id=c.propose_change(cid,"future","planned change",1789819200,1790180000,1790183600,"https://change.example/plan")
    direct_vm.warp("2026-09-23T16:15:00Z")
    out=c.review_change(change_id)
    assert out["result"]=="NOT_PERMITTED"
    assert c.get_change(change_id)["status"]=="EXPIRED_UNPERMITTED"


def test_duplicate_source_origins_are_not_independent(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice;direct_vm.value=10**18;direct_vm.warp("2026-09-19T12:00:00Z")
    sources=json.dumps([{"kind":"PROVIDER_STATUS","url":"https://same.example/status","note":"first"},{"kind":"INDEPENDENT_PROBE","url":"https://same.example/probe","note":"masquerading origin"}])
    with direct_vm.expect_revert("duplicate evidence origins"):
        c.create_covenant("API","https://api.example.com",1000,1000,9995,3600,1800,sources,REGISTRY,"independent public evidence",EXC,900)


def test_impossible_examination_intervals_are_rejected(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob);iid=verified_incident(direct_vm,c,rid,direct_bob)
    direct_vm.sender=direct_alice;c.claim_exception(iid,"UPSTREAM",UPSTREAM,"")
    direct_vm.mock_web(r".*",{"status":200,"body":"incident interval evidence"})
    malformed={"result":"VERIFIED","impact_start":1790001000,"impact_end":1790001000,"exception_start":1790002000,"exception_end":1790003000,"service_affected":True,"exception_event_established":True,"causal_link_supported":True,"clause_rule_satisfied":True,"permit_matches":False,"source_conflict":False,"basis":"impossible zero duration"}
    direct_vm.mock_llm(r".*",json.dumps(malformed))
    with pytest.raises(Exception,match="impossible incident interval"):
        c.examine_incident(iid)
    assert c.get_incident(iid)["status"]=="EXCEPTION_CLAIMED" and c.get_incident(iid)["liability_result"]==""


def test_challenge_parser_has_no_economic_liability_field(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid,iid=pending_liability(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_bob;direct_vm.value=10**16
    c.challenge_liability(iid,"The model must not choose the allocation.","https://counter.example/attempt");direct_vm.value=0
    direct_vm.mock_web(r".*",{"status":200,"body":"complete original and counter evidence"})
    direct_vm.mock_llm(r".*",json.dumps({"outcome":"UPHELD","revised_liable_bps":0,"basis":"attempt to choose payout"}))
    with pytest.raises(Exception):c.resolve_challenge(iid)
    incident=c.get_incident(iid)
    assert incident["liable_bps"]=="2945" and json.loads(incident["challenge"])["status"]=="OPEN"
    assert c.get_stats()["accounting_balanced"] is True


def test_exact_overlap_is_derived_from_timestamps(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid,iid=pending_liability(direct_vm,direct_deploy,direct_alice,direct_bob)
    incident=c.get_incident(iid)
    assert incident["examination"]["impact_start"]==1790001000
    assert incident["examination"]["impact_end"]==1790004600
    assert incident["examination"]["exception_start"]==1790002060
    assert incident["liable_bps"]=="2945"




def test_64_unadmitted_requests_cannot_lock_capacity_or_collateral(direct_vm,direct_deploy,direct_alice,direct_accounts):
    c=direct_deploy(CONTRACT);cid=create(direct_vm,c,direct_alice)
    customers=[create_address(f"headroom-spam-{i}") for i in range(64)]
    request_ids=[]
    for customer in customers:
        direct_vm.sender=customer
        request_ids.append(c.request_reservation(cid,1000,10**18,1790000000,1790180000,"unadmitted request"))
    assert len(request_ids)==64 and all(c.get_reservation(rid)["status"]=="PENDING_ADMISSION" for rid in request_ids)
    cv=c.get_covenant(cid)
    assert cv["reserved_units"]==0 and cv["reserved_liability_atto"]=="0" and cv["active_reservations"]==0
    direct_vm.sender=create_address("headroom-valid-requester")
    assert c.request_reservation(cid,1000,10**18,1790000000,1790180000,"eligible after spam")
    cv=c.get_covenant(cid)
    assert cv["reserved_units"]==0 and cv["reserved_liability_atto"]=="0"


def test_safe_admission_race_fails_headroom_changed(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
    c=direct_deploy(CONTRACT);cid=create(direct_vm,c,direct_alice)
    direct_vm.sender=direct_bob;first=c.request_reservation(cid,9000,9*10**18,1790000000,1790180000,"large promise")
    direct_vm.sender=direct_charlie;second=c.request_reservation(cid,1000,10**18,1790000000,1790180000,"racing promise")
    direct_vm.mock_web(r".*",{"status":200,"body":"healthy service and capacity"})
    direct_vm.mock_llm(r".*",json.dumps({"result":"SAFE","risk_state":"GREEN","service_healthy":True,"dependencies_healthy":True,"active_incident":False,"maintenance_conflict":False,"capacity_evidence_supports":True,"basis":"healthy now"}))
    c.review_reservation(first)
    direct_vm.clear_mocks();direct_vm.mock_web(r".*",{"status":200,"body":"healthy service and capacity"})
    direct_vm.mock_llm(r".*",json.dumps({"result":"SAFE","risk_state":"GREEN","service_healthy":True,"dependencies_healthy":True,"active_incident":False,"maintenance_conflict":False,"capacity_evidence_supports":True,"basis":"healthy now"}))
    out=c.review_reservation(second)
    assert out["result"]=="INCONCLUSIVE" and c.get_reservation(second)["status"]=="HEADROOM_CHANGED"
    cv=c.get_covenant(cid)
    assert cv["reserved_units"]==9000 and cv["reserved_liability_atto"]==str(9*10**18)


def test_pending_only_covenant_can_close_and_cannot_be_resurrected(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=direct_deploy(CONTRACT);cid=create(direct_vm,c,direct_alice);direct_vm.sender=direct_bob
    rid=c.request_reservation(cid,1000,10**18,1790000000,1790180000,"unadmitted")
    assert c.get_covenant(cid)["reserved_units"]==0
    direct_vm.sender=direct_alice;c.close_covenant(cid)
    assert c.get_covenant(cid)["status"]=="CLOSED"
    assert c.get_reservation(rid)["status"]=="CANCELLED_COVENANT_CLOSED"
    direct_vm.sender=direct_bob
    with direct_vm.expect_revert("covenant is not active"):
        c.review_reservation(rid)
    cv=c.get_covenant(cid)
    assert cv["reserved_units"]==0 and cv["reserved_liability_atto"]=="0" and cv["active_reservations"]==0
    assert c.get_stats()["accounting_balanced"] is True


def test_covenant_cannot_close_with_active_obligation(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_alice
    with direct_vm.expect_revert("cannot close with live obligations"):
        c.close_covenant(cid)
    assert c.get_covenant(cid)["status"]=="ACTIVE"
    assert c.get_covenant(cid)["reserved_units"]==1000


def test_change_review_lists_overlapping_frozen_sla_obligations(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_alice
    notice=1789819200;start=1790170000;end=start+3600
    change_id=c.propose_change(cid,"Regional failover","network route change",notice,start,end,"https://change.example/plan")
    direct_vm.mock_web(r".*",{"status":200,"body":"notice and window match; obligations protected"})
    direct_vm.mock_llm(r".*",json.dumps({"result":"PERMITTED","scope_matches":True,"notice_evidence_matches":True,"window_matches":True,"active_slas_protected":True,"dependency_risk_acceptable":True,"basis":"all evidence matches"}))
    c.review_change(change_id)
    change=c.get_change(change_id);case_hash=change["change_case_hash"]
    assert case_hash and change["status"]=="PERMITTED"
    assert len(change["review_obligations"])==1
    obligation=change["review_obligations"][0]
    assert obligation["id"]==rid and obligation["workload"]=="steady API workload"
    assert obligation["requested_units"]==1000 and obligation["sla"]["availability_target_bps"]==9995
    assert direct_vm.run_validator() is True


def test_challenge_liability_parser_cannot_select_liable_bps(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid,iid=pending_liability(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_bob;direct_vm.value=10**16
    c.challenge_liability(iid,"The model must not choose the allocation.","https://counter.example/attempt");direct_vm.value=0
    direct_vm.mock_web(r".*",{"status":200,"body":"complete original and counter evidence"})
    direct_vm.mock_llm(r".*",json.dumps({"outcome":"UPHELD","liable_bps":0,"basis":"direct economic choice"}))
    with pytest.raises(Exception):c.resolve_challenge(iid)
    assert c.get_incident(iid)["liable_bps"]=="2945"


def test_challenge_nondecision_preserves_liability_and_accounting(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid,iid=pending_liability(direct_vm,direct_deploy,direct_alice,direct_bob)
    before=c.get_incident(iid)["liable_bps"]
    direct_vm.sender=direct_bob;direct_vm.value=10**16
    c.challenge_liability(iid,"The event interval was wrong and must be reconstructed.","https://counter.example/evidence")
    direct_vm.value=0;direct_vm.mock_web(r".*",{"status":200,"body":""})
    result=c.resolve_challenge(iid)
    assert result["outcome"]=="SOURCE_UNAVAILABLE"
    after=c.get_incident(iid)
    assert after["liable_bps"]==before and after["liability_result"]=="PARTIAL"
    assert c.get_stats()["accounting_balanced"] is True


def test_challenge_refetches_original_measurement_exception_and_counter_sources(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid,iid=pending_liability(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_bob;direct_vm.value=10**16
    c.challenge_liability(iid,"The exception began later than recorded.","https://counter.example/evidence");direct_vm.value=0
    for pattern,body in [(r"probe\.example/incident","original measurement probe"),(r"status-archive\.example/incident","original measurement archive"),(r"status\.example/up","original exception record"),(r"counter\.example/evidence","challenge counter evidence")]:
        direct_vm.mock_web(pattern,{"status":200,"body":body})
    corrected={"result":"VERIFIED","impact_start":1790001000,"impact_end":1790004600,"exception_start":1790003000,"exception_end":1790004600,"service_affected":True,"exception_event_established":True,"causal_link_supported":True,"clause_rule_satisfied":True,"permit_matches":False,"source_conflict":False,"basis":"counter-evidence corrects event start"}
    direct_vm.mock_llm(r".*",json.dumps({"outcome":"UPHELD","corrected_examination":corrected,"basis":"reconstructed the full original case"}))
    result=c.resolve_challenge(iid)
    incident=c.get_incident(iid);stored=json.loads(incident["challenge"])
    assert stored["status"]=="UPHELD"
    assert incident["examination"]["exception_start"]==1790003000
    assert incident["liable_bps"]=="5556"
    assert incident["liability_result"]=="PARTIAL"
    assert result["liable_bps"]==5556
    assert incident["settlement_case_hash"] and incident["challenge_case_hash"]
    assert direct_vm._web_mocks_hit=={0,1,2,3}
    direct_vm.warp("2026-09-21T15:46:00Z");c.finalize_incident(iid)
    final=c.get_incident(iid);certificate=final["settlement_certificate"]
    assert certificate["liability_result"]==final["liability_result"]=="PARTIAL"
    assert certificate["liable_bps"]==int(final["liable_bps"])==5556
    assert certificate["examination"]==final["examination"]
    assert certificate["challenge_case_hash"]==final["challenge_case_hash"]
    assert final["settlement_hash"]==hashlib.sha256(json.dumps(certificate,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    assert c.get_stats()["accounting_balanced"] is True


def test_challenge_refetches_original_permit_record_and_evidence(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=direct_deploy(CONTRACT);cid=create(direct_vm,c,direct_alice)
    direct_vm.sender=direct_alice
    window_start=1790002500;window_end=1790003500
    change_id=c.propose_change(cid,"Planned maintenance","rolling database failover",1789819200,window_start,window_end,"https://change.example/plan")
    direct_vm.mock_web(r"change\.example/plan",{"status":200,"body":"notice, scope, and exact approved window"})
    direct_vm.mock_llm(r".*",json.dumps({"result":"PERMITTED","scope_matches":True,"notice_evidence_matches":True,"window_matches":True,"active_slas_protected":True,"dependency_risk_acceptable":True,"basis":"notice and protected obligations match"}))
    c.review_change(change_id);direct_vm.clear_mocks()
    direct_vm.sender=direct_bob
    rid=c.request_reservation(cid,1000,10**18,1790000000,1790180000,"steady API workload")
    direct_vm.mock_web(r".*",{"status":200,"body":"service and dependencies healthy"})
    direct_vm.mock_llm(r".*",json.dumps({"result":"SAFE","risk_state":"GREEN","service_healthy":True,"dependencies_healthy":True,"active_incident":False,"maintenance_conflict":False,"capacity_evidence_supports":True,"basis":"healthy now"}))
    c.review_reservation(rid);direct_vm.clear_mocks()
    direct_vm.warp("2026-09-21T15:30:00Z")
    iid=c.open_incident(rid,9900,1790001000,1790004600,MEASUREMENT)
    direct_vm.mock_web(r".*",{"status":200,"body":"measured service failure in exact incident window"})
    direct_vm.mock_llm(r".*",json.dumps({"result":"VERIFIED","measured_bps":9900,"service_matches":True,"window_matches":True,"basis":"measurement established"}))
    c.verify_incident_measurement(iid);direct_vm.clear_mocks()
    direct_vm.sender=direct_alice
    c.claim_exception(iid,"MAINT",UPSTREAM,change_id)
    direct_vm.mock_web(r".*",{"status":200,"body":"maintenance event and causal impact timelines"})
    exam={"result":"VERIFIED","impact_start":1790001000,"impact_end":1790004600,"exception_start":1790003000,"exception_end":1790003500,"service_affected":True,"exception_event_established":True,"causal_link_supported":True,"clause_rule_satisfied":True,"permit_matches":True,"source_conflict":False,"basis":"permit covers the verified maintenance interval"}
    direct_vm.mock_llm(r".*",json.dumps(exam));c.examine_incident(iid);c.judge_liability(iid);direct_vm.clear_mocks()
    direct_vm.sender=direct_bob;direct_vm.value=10**16
    c.challenge_liability(iid,"The event was not causally connected.","https://counter.example/evidence");direct_vm.value=0
    for pattern,body in [(r"probe\.example/incident","original measurement probe"),(r"status-archive\.example/incident","original measurement archive"),(r"status\.example/up","original exception evidence"),(r"change\.example/plan","frozen permit evidence"),(r"counter\.example/evidence","challenge counter evidence")]:
        direct_vm.mock_web(pattern,{"status":200,"body":body})
    direct_vm.mock_llm(r".*",json.dumps({"outcome":"REJECTED","corrected_examination":None,"basis":"full case reconstruction supports the original facts"}))
    result=c.resolve_challenge(iid)
    assert result["outcome"]=="REJECTED" and c.get_incident(iid)["challenge_case_hash"]
    assert direct_vm._web_mocks_hit=={0,1,2,3,4}
    assert c.get_incident(iid)["permitted_change"]["permit_hash"]==c.get_change(change_id)["permit_hash"]
    assert c.get_stats()["accounting_balanced"] is True


def test_challenge_validator_disagreement_rejects_candidate(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid,iid=pending_liability(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_bob;direct_vm.value=10**16
    c.challenge_liability(iid,"The initial facts are correct.","https://counter.example/disagreement");direct_vm.value=0
    direct_vm.mock_web(r".*",{"status":200,"body":"complete case and counter evidence"})
    direct_vm.mock_llm(r".*",json.dumps({"outcome":"REJECTED","corrected_examination":None,"basis":"original facts stand"}))
    c.resolve_challenge(iid);direct_vm.clear_mocks()
    corrected={"result":"VERIFIED","impact_start":1790001000,"impact_end":1790004600,"exception_start":1790003000,"exception_end":1790004600,"service_affected":True,"exception_event_established":True,"causal_link_supported":True,"clause_rule_satisfied":True,"permit_matches":False,"source_conflict":False,"basis":"conflicting validator evidence"}
    direct_vm.mock_web(r".*",{"status":200,"body":"validator's contradictory case reconstruction"})
    direct_vm.mock_llm(r".*",json.dumps({"outcome":"UPHELD","corrected_examination":corrected,"basis":"conflicting result"}))
    assert direct_vm.run_validator() is False
    incident=c.get_incident(iid)
    assert incident["liable_bps"]=="2945" and incident["liability_result"]=="PARTIAL"
    assert json.loads(incident["challenge"])["status"]=="REJECTED"
    assert c.get_stats()["accounting_balanced"] is True


def test_future_incident_observation_is_rejected(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_bob
    now=1790007000
    with direct_vm.expect_revert("cannot be future"):
        c.open_incident(rid,9900,now+10,now+3610,MEASUREMENT)


def test_permit_requires_incident_time_overlap_and_same_covenant(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob);iid=verified_incident(direct_vm,c,rid,direct_bob)
    direct_vm.sender=direct_alice
    notice=1789819200;start=1790180000;end=start+1800
    change_id=c.propose_change(cid,"later work","outside incident window",notice,start,end,"https://change.example/later")
    direct_vm.mock_web(r".*",{"status":200,"body":"public notice for a later window"})
    direct_vm.mock_llm(r".*",json.dumps({"result":"PERMITTED","scope_matches":True,"notice_evidence_matches":True,"window_matches":True,"active_slas_protected":True,"dependency_risk_acceptable":True,"basis":"future maintenance is acceptable"}))
    c.review_change(change_id)
    assert c.get_change(change_id)["status"]=="PERMITTED"
    direct_vm.sender=direct_alice
    with direct_vm.expect_revert("does not match this covenant and incident timing"):
        c.claim_exception(iid,"MAINT",UPSTREAM,change_id)
    direct_vm.clear_mocks()


def test_unrelated_covenant_permit_cannot_be_used(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob);iid=verified_incident(direct_vm,c,rid,direct_bob)
    direct_vm.sender=direct_alice;other=create(direct_vm,c,direct_charlie)
    direct_vm.sender=direct_charlie
    ch=c.propose_change(other,"unrelated","different service",1789819200,1790180000,1790181800,"https://change.example/unrelated")
    direct_vm.mock_web(r".*",{"status":200,"body":"notice and window"})
    direct_vm.mock_llm(r".*",json.dumps({"result":"PERMITTED","scope_matches":True,"notice_evidence_matches":True,"window_matches":True,"active_slas_protected":True,"dependency_risk_acceptable":True,"basis":"approved"}))
    c.review_change(ch);direct_vm.sender=direct_alice
    with direct_vm.expect_revert("does not match this covenant"):
        c.claim_exception(iid,"MAINT",UPSTREAM,ch)


def test_malformed_leader_result_fails_without_economic_decision(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=direct_deploy(CONTRACT);cid=create(direct_vm,c,direct_alice);direct_vm.sender=direct_bob
    rid=c.request_reservation(cid,1000,10**18,1790000000,1790180000,"valid future workload")
    direct_vm.mock_web(r".*",{"status":200,"body":"healthy"});direct_vm.mock_llm(r".*","not-json")
    with pytest.raises(Exception):c.review_reservation(rid)
    assert c.get_reservation(rid)["status"]=="PENDING_ADMISSION"
    assert c.get_covenant(cid)["reserved_units"]==0


def test_validator_source_failure_rejects_candidate(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=direct_deploy(CONTRACT);cid=create(direct_vm,c,direct_alice);direct_vm.sender=direct_bob
    rid=c.request_reservation(cid,1000,10**18,1790000000,1790180000,"valid future workload")
    direct_vm.mock_web(r".*",{"status":200,"body":"healthy evidence"})
    direct_vm.mock_llm(r".*",json.dumps({"result":"SAFE","risk_state":"GREEN","service_healthy":True,"dependencies_healthy":True,"active_incident":False,"maintenance_conflict":False,"capacity_evidence_supports":True,"basis":"healthy"}))
    c.review_reservation(rid);direct_vm.clear_mocks();direct_vm.mock_web(r".*",{"status":200,"body":""})
    assert direct_vm.run_validator() is False
    assert c.get_reservation(rid)["status"]=="ACTIVE"


def test_final_settlement_certificate_matches_adjudication(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid,iid=pending_liability(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.warp("2026-09-21T15:46:00Z")
    c.finalize_incident(iid)
    incident=c.get_incident(iid);certificate=incident["settlement_certificate"]
    assert incident["liability_result"]=="PARTIAL" and incident["liable_bps"]=="2945"
    assert certificate["liable_bps"]==2945 and certificate["liability_result"]=="PARTIAL"
    assert incident["settlement_hash"]==hashlib.sha256(json.dumps(certificate,sort_keys=True,separators=(",",":")).encode()).hexdigest() and incident["payout_atto"]==str(2945*10**14)
    assert c.get_stats()["accounting_balanced"] is True


def test_unresolved_challenge_refund_keeps_settlement_finalizable(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid,iid=pending_liability(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_bob;direct_vm.value=10**16
    c.challenge_liability(iid,"Evidence is unavailable and should time out safely.","https://counter.example/missing");direct_vm.value=0
    before=c.get_incident(iid)["liable_bps"]
    direct_vm.warp("2026-09-24T00:00:00Z");c.expire_challenge(iid)
    assert c.get_incident(iid)["liable_bps"]==before
    assert c.get_stats()["accounting_balanced"] is True
    direct_vm.warp("2026-09-24T00:15:00Z");c.finalize_incident(iid)
    assert c.get_incident(iid)["status"]=="FINAL"
    assert c.get_stats()["accounting_balanced"] is True


def test_timeout_default_certificate_contains_full_case(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob);iid=verified_incident(direct_vm,c,rid,direct_bob)
    direct_vm.warp("2026-09-21T16:31:00Z");c.finalize_default_breach(iid)
    incident=c.get_incident(iid);cert=incident["settlement_certificate"]
    assert cert["liability_result"]=="DEFAULT_LIABLE" and cert["liable_bps"]==10000
    assert cert["examination"]=={}
    assert incident["settlement_hash"]==hashlib.sha256(json.dumps(cert,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    assert c.get_stats()["accounting_balanced"] is True


def test_arbitrary_origin_cannot_self_label_independent_probe(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice;direct_vm.value=10**18;direct_vm.warp("2026-09-19T12:00:00Z")
    sources=json.dumps([{"kind":"PROVIDER_STATUS","url":"https://service.example/status","note":"provider status"},{"kind":"INDEPENDENT_PROBE","url":"https://attacker.example/probe","note":"self declared probe"}])
    with direct_vm.expect_revert("origin/class is not authorized"):
        c.create_covenant("API","https://api.example.com",1000,1000,9995,3600,1800,sources,REGISTRY,"public evidence policy",EXC,900)

def test_provider_controlled_origin_cannot_be_registered_as_independent(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice;direct_vm.value=10**18;direct_vm.warp("2026-09-19T12:00:00Z")
    registry=json.dumps([{"kind":"INDEPENDENT_PROBE","origin":"https://api.example.com"},{"kind":"PROVIDER_STATUS","origin":"https://service.example"}])
    with direct_vm.expect_revert("service origin is provider-controlled"):
        c.create_covenant("API","https://api.example.com",1000,1000,9995,3600,1800,SOURCES,registry,"public evidence policy",EXC,900)

def test_frozen_origin_with_wrong_class_is_rejected_for_measurement(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob)
    wrong=json.dumps([{"kind":"INDEPENDENT_PROBE","url":"https://probe.example/incident","note":"probe"},{"kind":"PUBLIC_TELEMETRY","url":"https://status-archive.example/incident","note":"wrong class for registered origin"}])
    with direct_vm.expect_revert("origin/class is not authorized"):
        c.open_incident(rid,9900,1790001000,1790004600,wrong)

def test_correct_frozen_origin_class_is_accepted(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob)
    iid=c.open_incident(rid,9900,1790001000,1790004600,MEASUREMENT)
    assert c.get_incident(iid)["status"]=="MEASUREMENT_PENDING"

def test_source_registry_rejects_duplicate_origin_across_classes(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice;direct_vm.value=10**18;direct_vm.warp("2026-09-19T12:00:00Z")
    registry=json.dumps([{"kind":"PROVIDER_STATUS","origin":"https://service.example"},{"kind":"INDEPENDENT_PROBE","origin":"https://service.example"}])
    with direct_vm.expect_revert("origin may be registered only once"):
        c.create_covenant("API","https://api.example.com",1000,1000,9995,3600,1800,SOURCES,registry,"public evidence policy",EXC,900)


def test_change_evidence_must_use_its_frozen_class(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);cid=create(direct_vm,c,direct_alice);direct_vm.sender=direct_alice
    start=1790000000;end=start+1800;notice=1789819200
    with direct_vm.expect_revert("origin/class is not authorized"):
        c.propose_change(cid,"Planned change","online migration",notice,start,end,"https://status-archive.example/plan")

def test_exception_evidence_must_use_its_frozen_class(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob);iid=verified_incident(direct_vm,c,rid,direct_bob)
    direct_vm.sender=direct_alice
    wrong=json.dumps([{"kind":"UPSTREAM_STATUS","url":"https://status-archive.example/wrong-class","note":"origin is registered only as aggregator"}])
    with direct_vm.expect_revert("origin/class is not authorized"):
        c.claim_exception(iid,"UPSTREAM",wrong,"")

def test_challenge_evidence_requires_frozen_challenge_class(direct_vm,direct_deploy,direct_alice,direct_bob):
    registry_items=json.loads(REGISTRY)
    registry_items=[dict(x,kind="STATUS_AGGREGATOR") if x["origin"]=="https://counter.example" else x for x in registry_items]
    wrong_registry=json.dumps(registry_items)
    c,cid,rid,iid=pending_liability(direct_vm,direct_deploy,direct_alice,direct_bob,wrong_registry)
    direct_vm.sender=direct_bob;direct_vm.value=10**16
    with direct_vm.expect_revert("origin/class is not authorized"):
        c.challenge_liability(iid,"wrongly classified counter evidence","https://counter.example/evidence")



