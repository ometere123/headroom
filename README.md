# HEADROOM

**A preventive SLA admission and enforcement protocol: unsafe promises and unsafe changes are blocked before formation; if prevention still fails, the same frozen covenant adjudicates the incident and settles reserved liability.**

HEADROOM is hard-locked to **GenLayer Studionet only**:

- chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- wallet: generic injected **EIP-1193** through `window.ethereum` only

There is no 61997/Studio-dev release path, Snaps path, WalletConnect path, embedded wallet, backend signer or browser private key in the application.

## Product boundary

HEADROOM is the flagship. It uses the same covenant twice: before risk exists, GenLayer and deterministic collateral/capacity gates decide whether a new SLA promise or operational change may proceed; after a verified miss, the covenant becomes the incident law. The customer cannot self-create liability, the provider cannot self-excuse, and the model never invents the payout.

Changing web evidence and semantic questions use custom leader/validator consensus. Validators independently re-fetch/reason and compare consequential structured fields rather than accepting JSON shape or free-form prose. Threshold arithmetic, escrow, credits, time windows and final settlement remain deterministic.

## Main lifecycle

`create_covenant → request_reservation → review_reservation → propose_change/review_change → open_incident → verify_incident_measurement → claim_exception → examine_incident → judge_liability → optional challenge_liability/resolve_challenge → finalize_incident (or bounded default breach) → withdraw_credit`

## Repository

```text
contracts/headroom.py       one substantial Intelligent Contract
22 Direct Mode tests        authored behavioural/adversarial coverage
tests/integration/              opt-in live Studionet smoke against a deployed address
frontend/                       multipage Next.js application
deploy/deployScript.ts          61999-locked deployment script
docs/                           architecture, security, live-demo and reviewer evidence
AGENT_HANDOFF.md                detailed execution handoff
GOAL_PROMPT.txt                 compact finishing-agent goal
STATIC_VERIFICATION.md          checks actually run while packaging
```

Current contract surface: **29 public methods**, **458 source lines**.

## Frontend

The UI is intentionally product-specific rather than a reusable crypto/AI dashboard. Visual direction: **contractual operations control room: dark promise-surface console, capacity/liability block gauges, admission lanes, change-control signals and forensic incident timelines**.

Routes: `/`, `/covenants`, `/covenants/[id]`, `/open`, `/account`, `/protocol`. The dynamic detail route reads finalized on-chain state and exposes the complete protocol write path with signing/finalizing/finalized/error feedback.

## Static checks included in the handoff

```bash
python -m py_compile contracts/headroom.py tests/direct/*.py tests/integration/*.py
python scripts/check_contract_patterns.py
python scripts/check_release.py
```

The packaging pass also parses every current frontend `.ts`/`.tsx` file with the TypeScript compiler API. See `STATIC_VERIFICATION.md`.

## Real release gates for the finishing environment

```bash
pip install -r requirements.txt
genvm-lint check contracts/headroom.py --json
pytest tests/direct/ -v
cd frontend && npm install && npm run typecheck && npm run build
```

Then confirm the built-in network resolves to **61999** / `https://studio.genlayer.com/api`, deploy the exact final source, wait for FINALIZED plus successful execution, compare deployed schema/source with this repository, wire the finalized address into the frontend, publish it, and run `docs/LIVE_DEMO.md` with real evidence and real transaction hashes.

## Release honesty

This ZIP is a source-complete implementation handoff, not a fabricated deployment report. The packaging environment did not have the GenLayer Python toolchain or frontend dependency tree available, so it does **not** claim `genvm-lint`, executed Direct Mode, Next production build, deployment, live validator consensus, native GEN settlement or public hosting. `VERIFICATION_STATUS.md` and `STATIC_VERIFICATION.md` separate what was actually checked from what the finishing agent must prove.
