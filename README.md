# HEADROOM

**A preventive SLA admission and enforcement protocol.** HEADROOM establishes consensus before risk: deterministic capacity and collateral rules reject impossible promises before semantic admission, and unsafe operating changes are blocked before their windows. If prevention fails, consensus establishes incident facts and contract code computes settlement deterministically.

HEADROOM is hard-locked to GenLayer Studionet:

- Chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- Wallet: generic injected EIP-1193 through `window.ethereum`

The application has no 61997/Studio-dev path, embedded signer, backend signer, browser private key, WalletConnect or Snaps integration.

## Lifecycle

`create_covenant → request_reservation → review_reservation → propose_change/review_change → open_incident → verify_incident_measurement → claim_exception → examine_incident → judge_liability → optional challenge_liability/resolve_challenge → finalize_incident → withdraw_credit`

Reservation requests first receive deterministic capacity and collateral checks. Failed checks are stored as `DENIED_DETERMINISTIC` and never reach web/LLM admission. Pending requests hold no capacity or collateral. A SAFE semantic result activates only after a fresh headroom check.

Each covenant freezes HTTPS origins and evidence classes. A URL is accepted only when its submitted origin and declared class are authorized. Origins must be distinct where independent sources are required. GenLayer does not expose redirect destinations, so HEADROOM makes no claim about the origin of redirected content.

Incident consensus returns bounded timestamps and structured facts. `judge_liability()` computes temporal overlap and provider liability from those facts; an LLM never selects a payout percentage. Challenges re-fetch the original evidence and apply the same deterministic liability law to corrected facts.

## Repository

- `contracts/headroom.py`: single intelligent contract
- `tests/direct/`: Direct Mode adversarial suite
- `tests/integration/`: opt-in live Studionet smoke test
- `frontend/`: control-room UI
- `deploy/`: chain-locked deployment script
- `docs/`: architecture, security, environment and reviewer evidence

Source-derived facts: **609 contract lines**, **10 public views**, **21 public writes**, **54 Direct Mode tests**. These counts are computed from the current source in `scripts/update_verification_facts.py` when documentation is refreshed.

## Local gates

```bash
python -m py_compile contracts/headroom.py tests/direct/*.py tests/integration/*.py
python scripts/check_genvm_lint.py
pytest tests/direct/ -v
python scripts/check_release.py
python scripts/check_contract_patterns.py
python scripts/check_frontend_surface.py
cd frontend && npm install && npm run typecheck && npm run build
```

See [verification status](VERIFICATION_STATUS.md), [static verification](STATIC_VERIFICATION.md), and [review evidence](docs/REVIEW_EVIDENCE.md). CI runs the same gates. The current GitHub Actions result is linked from the review evidence.

## Deployment status

No deployment or live Studionet lifecycle proof is claimed. The next phase requires real independent consensus evidence, a complete live lifecycle, frontend wiring to the deployed address, and reviewer evidence.
