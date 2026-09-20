import json
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


def create(vm, c, provider, bond=10 * 10**18):
    vm.sender = provider
    vm.value = bond
    vm.warp("2026-09-19T12:00:00Z")
    cid = c.create_covenant(
        "Payments EU", "https://api.example.com", 10000, 1000, 9995,
        172800, 7200, SOURCES,
        "Admission requires live provider and independent evidence. Incident causation requires public timeline evidence.",
        EXC, 900,
    )
    vm.value = 0
    return cid


def active_reservation(vm, deploy, provider, customer, credit=10**18):
    c = deploy(CONTRACT)
    cid = create(vm, c, provider)
    vm.sender = customer
    rid = c.request_reservation(cid, 1000, credit, 1789819200, 1790000000, "steady API workload")
    vm.mock_web(r".*", {"status":200, "body":"Payments EU healthy. No active incident. Independent probe healthy. Capacity remains within declared envelope."})
    vm.mock_llm(r".*", json.dumps({
        "result":"SAFE", "risk_state":"GREEN", "service_healthy":True,
        "dependencies_healthy":True, "active_incident":False, "maintenance_conflict":False,
        "capacity_evidence_supports":True, "basis":"provider and independent evidence agree",
    }))
    out = c.review_reservation(rid)
    assert out["result"] == "SAFE"
    vm.clear_mocks()
    return c, cid, rid


def verified_incident(vm, c, rid, customer, measured=9900):
    vm.sender = customer
    iid = c.open_incident(rid, measured, 1789820000, 1789823600, MEASUREMENT)
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


def pending_liability(vm, deploy, provider, customer):
    c, cid, rid = active_reservation(vm, deploy, provider, customer)
    iid = verified_incident(vm, c, rid, customer)
    vm.sender = provider
    c.claim_exception(iid, "UPSTREAM", UPSTREAM, "")
    vm.mock_web(r".*", {"status":200, "body":"Customer impact 12:13-13:13. Upstream incident 12:31-13:13. Evidence supports causal overlap after 12:31."})
    vm.mock_llm(r".*", json.dumps({
        "result":"VERIFIED", "impact_start":1789820000, "impact_end":1789823600,
        "exception_start":1789821060, "exception_end":1789823600, "causal_overlap_bps":7000,
        "service_affected":True, "exception_event_established":True, "causal_link_supported":True,
        "clause_rule_satisfied":True, "permit_matches":False, "source_conflict":False, "basis":"bounded causal overlap established",
    }))
    c.examine_incident(iid)
    vm.clear_mocks()
    out = c.judge_liability(iid)
    assert out["result"] == "PARTIAL"
    assert out["liable_bps"] == 3000
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
        c.create_covenant("API", "https://api.example.com", 1000, 1000, 9995, 3600, 1800, bad, "public evidence policy", EXC, 900)


def test_capacity_precheck_prevents_overpromise(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice); direct_vm.sender = direct_bob
    rid = c.request_reservation(cid, 9500, 10**18, 1789819200, 1790000000, "large workload")
    assert c.get_reservation(rid)["status"] == "DENIED_DETERMINISTIC"
    assert c.get_stats()["prevented"] == 1


def test_liability_precheck_prevents_uncollateralized_promise(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice, bond=10**18); direct_vm.sender = direct_bob
    rid = c.request_reservation(cid, 1000, 2 * 10**18, 1789819200, 1790000000, "normal workload")
    r = c.get_reservation(rid)
    assert r["liability_precheck"] is False and r["status"] == "DENIED_DETERMINISTIC"


def test_live_safe_admission_reserves_capacity_and_liability(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    cv = c.get_covenant(cid)
    assert cv["reserved_units"] == 1000
    assert cv["reserved_liability_atto"] == str(10**18)
    assert c.get_reservation(rid)["admission_hash"]


def test_admission_validator_rechecks_substantive_live_state(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice); direct_vm.sender = direct_bob
    rid = c.request_reservation(cid, 1000, 10**18, 1789819200, 1790000000, "normal workload")
    direct_vm.mock_web(r".*", {"status":200, "body":"healthy"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"SAFE","risk_state":"GREEN","service_healthy":True,"dependencies_healthy":True,"active_incident":False,"maintenance_conflict":False,"capacity_evidence_supports":True,"basis":"healthy"}))
    c.review_reservation(rid)
    direct_vm.clear_mocks()
    direct_vm.mock_web(r".*", {"status":200, "body":"active regional incident"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"UNSAFE","risk_state":"RED","service_healthy":False,"dependencies_healthy":False,"active_incident":True,"maintenance_conflict":False,"capacity_evidence_supports":False,"basis":"incident"}))
    assert direct_vm.run_validator() is False


def test_live_unsafe_admission_is_prevented(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice); direct_vm.sender = direct_bob
    rid = c.request_reservation(cid, 1000, 10**18, 1789819200, 1790000000, "normal workload")
    direct_vm.mock_web(r".*", {"status":200, "body":"active regional incident"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"UNSAFE","risk_state":"RED","service_healthy":False,"dependencies_healthy":False,"active_incident":True,"maintenance_conflict":False,"capacity_evidence_supports":False,"basis":"active incident"}))
    c.review_reservation(rid)
    assert c.get_reservation(rid)["status"] == "DENIED_LIVE"


def test_change_without_notice_is_blocked_before_ai(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy(CONTRACT); cid = create(direct_vm, c, direct_alice); direct_vm.sender = direct_alice
    chg = c.propose_change(cid, "DB migration", "online schema change", 1789819000, 1789820000, 1789823600, "https://change.example/plan")
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
        c.open_incident(rid, 9995, 1789820000, 1789823600, MEASUREMENT)


def test_exception_path_cannot_open_before_measurement_consensus(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_bob; iid = c.open_incident(rid, 9900, 1789820000, 1789823600, MEASUREMENT)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("provider cannot invoke exception"):
        c.claim_exception(iid, "UPSTREAM", UPSTREAM, "")


def test_measurement_validator_replays_evidence_and_metric(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_bob; iid = c.open_incident(rid, 9900, 1789820000, 1789823600, MEASUREMENT)
    direct_vm.mock_web(r".*", {"status":200, "body":"99.00% exact window"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"VERIFIED","measured_bps":9900,"service_matches":True,"window_matches":True,"basis":"exact"}))
    c.verify_incident_measurement(iid)
    direct_vm.clear_mocks(); direct_vm.mock_web(r".*", {"status":200, "body":"99.80%"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"VERIFIED","measured_bps":9980,"service_matches":True,"window_matches":True,"basis":"different"}))
    assert direct_vm.run_validator() is False


def test_measurement_not_proven_does_not_create_liability(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_bob; iid = c.open_incident(rid, 9900, 1789820000, 1789823600, MEASUREMENT)
    direct_vm.mock_web(r".*", {"status":200, "body":"unrelated service"})
    direct_vm.mock_llm(r".*", json.dumps({"result":"NOT_PROVEN","measured_bps":0,"service_matches":False,"window_matches":False,"basis":"wrong service"}))
    c.verify_incident_measurement(iid)
    assert c.get_incident(iid)["status"] == "MEASUREMENT_REJECTED"
    assert c.get_reservation(rid)["incident_id"] == ""


def test_unavailable_measurement_has_bounded_liveness_and_can_be_dismissed(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_bob; iid = c.open_incident(rid, 9900, 1789820000, 1789823600, MEASUREMENT)
    direct_vm.mock_web(r".*", {"status":200, "body":""})
    assert c.verify_incident_measurement(iid)["result"] == "SOURCE_UNAVAILABLE"
    direct_vm.warp("2026-09-19T18:01:00Z")
    c.dismiss_unproven_measurement(iid)
    assert c.get_incident(iid)["status"] == "MEASUREMENT_REJECTED"
    assert c.get_reservation(rid)["incident_id"] == ""


def test_unanswered_verified_incident_defaults_to_reserved_credit(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    iid = verified_incident(direct_vm, c, rid, direct_bob)
    direct_vm.warp("2026-09-19T13:01:00Z"); direct_vm.sender = direct_bob
    out = c.finalize_default_breach(iid)
    assert out["liable_bps"] == 10000
    assert c.get_incident(iid)["status"] == "FINAL"
    assert c.get_credit(hx(direct_bob)) == str(10**18)
    assert c.get_stats()["accounting_balanced"] is True


def test_provider_cannot_invoke_exception_after_response_deadline(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid = active_reservation(direct_vm, direct_deploy, direct_alice, direct_bob)
    iid = verified_incident(direct_vm, c, rid, direct_bob)
    direct_vm.warp("2026-09-19T13:01:00Z"); direct_vm.sender = direct_alice
    with direct_vm.expect_revert("provider cannot invoke exception"):
        c.claim_exception(iid, "UPSTREAM", UPSTREAM, "")


def test_partial_causation_moves_only_deterministically_calculated_credit(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid, iid = pending_liability(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.warp("2026-09-19T12:16:00Z")
    out = c.finalize_incident(iid)
    assert out["liable_bps"] == 3000
    assert out["payout_atto"] == str(3 * 10**17)
    assert c.get_credit(hx(direct_bob)) == str(3 * 10**17)
    assert c.get_stats()["accounting_balanced"] is True


def test_undecidable_challenge_cannot_grief_settlement_forever(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, cid, rid, iid = pending_liability(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_bob; direct_vm.value = 10**16
    c.challenge_liability(iid, "Upstream incident began after customer impact.", "https://counter.example/evidence")
    direct_vm.value = 0
    direct_vm.mock_web(r".*", {"status":200, "body":""})
    assert c.resolve_challenge(iid)["outcome"] == "SOURCE_UNAVAILABLE"
    direct_vm.warp("2026-09-20T13:00:00Z")
    c.expire_challenge(iid)
    ch = json.loads(c.get_incident(iid)["challenge"])
    assert ch["status"] == "EXPIRED"
    assert c.get_credit(hx(direct_bob)) == str(10**16)


def test_stats_expose_prevention_and_no_admin(direct_vm, direct_deploy):
    s = direct_deploy(CONTRACT).get_stats()
    assert s["chain_id"] == "61999"
    assert s["rpc"] == "https://studio.genlayer.com/api"
    assert s["admin_controls"] is False


def test_incident_measurement_requires_independent_probe_and_second_source_family(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid,rid=active_reservation(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_bob
    one=json.dumps([{"kind":"INDEPENDENT_PROBE","url":"https://probe.example/only","note":"single source"}])
    with direct_vm.expect_revert("use 2"):
        c.open_incident(rid,9900,1789820000,1789823600,one)
    same=json.dumps([{"kind":"INDEPENDENT_PROBE","url":"https://probe-a.example/x","note":"probe a"},{"kind":"INDEPENDENT_PROBE","url":"https://probe-b.example/x","note":"probe b"}])
    with direct_vm.expect_revert("two source families"):
        c.open_incident(rid,9900,1789820000,1789823600,same)


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
        "result":"VERIFIED","impact_start":1789820000,"impact_end":1789823600,
        "exception_start":1789821060,"exception_end":1789823600,"causal_overlap_bps":7000,
        "service_affected":True,"exception_event_established":True,"causal_link_supported":True,
        "clause_rule_satisfied":False,"permit_matches":False,"source_conflict":False,
        "basis":"event exists but frozen contractual condition is not satisfied",
    }))
    c.examine_incident(iid);direct_vm.clear_mocks()
    out=c.judge_liability(iid)
    assert out["result"]=="LIABLE"
    assert out["liable_bps"]==10000
