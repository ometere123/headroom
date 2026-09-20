"""Run GenVM validation and allow only the reviewed custom-consensus E010 set."""

import json
import subprocess
import sys

command = ["genvm-lint", "check", "contracts/headroom.py", "--json"]
result = subprocess.run(command, text=True, capture_output=True)
sys.stdout.write(result.stdout)
sys.stderr.write(result.stderr)
if result.returncode == 0:
    raise SystemExit(0)

try:
    report = json.loads(result.stdout)
except json.JSONDecodeError as exc:
    print(f"Unable to parse genvm-lint JSON output: {exc}", file=sys.stderr)
    raise SystemExit(result.returncode)

expected = {
    "gl.nondet.* call in '_fetch' not reachable from equivalence principle block": 1,
    "gl.nondet.* call in 'Headroom.review_reservation.<locals>.leader_fn' not reachable from equivalence principle block": 1,
    "gl.nondet.* call in 'Headroom.review_change.<locals>.leader_fn' not reachable from equivalence principle block": 2,
    "gl.nondet.* call in 'Headroom.verify_incident_measurement.<locals>.leader_fn' not reachable from equivalence principle block": 1,
    "gl.nondet.* call in 'Headroom.examine_incident.<locals>.leader_fn' not reachable from equivalence principle block": 1,
    "gl.nondet.* call in 'Headroom.resolve_challenge.<locals>.leader_fn' not reachable from equivalence principle block": 1,
}
warnings = report.get("lint", {}).get("warnings", [])
actual = {}
for warning in warnings:
    message = warning.get("msg", "")
    actual[message] = actual.get(message, 0) + 1

if report.get("validate", {}).get("ok") is not True:
    print("GenVM contract validation failed.", file=sys.stderr)
    raise SystemExit(1)
if any(warning.get("code") != "E010" for warning in warnings) or actual != expected:
    print("GenVM lint warnings differ from the explicitly reviewed E010 set.", file=sys.stderr)
    raise SystemExit(1)

print("Accepted reviewed E010 custom run_nondet_unsafe reachability warnings; contract validation passed.")
