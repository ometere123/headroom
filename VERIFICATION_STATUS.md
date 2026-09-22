# Verification Status

## Canonical contract

The deployed Studionet contract `0x235Fd204E6d78e61055a6BD24B06319aA503D2f1` was finalized successfully by transaction `0x99114e7506ca30f35ee1c9bc1f81c7147c56f305fb49c0bed97071c5a1e7545e`. Deployed source SHA-256 is `a61cb6815251ac3f118fb73fe81c9e10b7575c13ab3135e7664ebcdd9b587dbd`, matching repository `contracts/headroom.py` at source commit `add2f35d08cde554bec6d9bed98c5094554035d9`. Its schema is 10 views and 21 writes. Live `get_stats()` reports Studionet, chain 61999, balanced accounting, and no admin controls.

## Candidate checks

Record the results for the exact release commit here and in [review evidence](docs/REVIEW_EVIDENCE.md):

- Python 3.12.3 compile: PASS (`contracts/headroom.py`, all direct and integration test modules).
- GenVM validation: `genvm-linter==0.11.1rc2`; the reviewed exact seven E010 custom validator diagnostics remain the only accepted warnings.
- Direct Mode: PASS, 57 passed (`genlayer-test==0.29.2`, `genlayer-py==0.16.3`).
- `check_release.py`, `check_contract_patterns.py`, `check_frontend_surface.py`: PASS.
- Frontend SDK: exact `genlayer-js==1.1.8`; `npm run typecheck` and `npm run build`: PASS.
- GitHub Actions on release source `add2f35d08cde554bec6d9bed98c5094554035d9`: PASS, [run 35690301279](https://github.com/ometere123/headroom/actions/runs/35690301279); full Direct Mode and frontend build passed.
- Vercel Production: existing project linked; four required Production variables confirmed; deployment READY at https://the-headroom.vercel.app/ and browser walkthrough completed for routes, live reads, wallet connection and chain state.

## Live protocol evidence

The deployment is verified and live proof is now present. `hr-cv-3` is active, `hr-r-1` proves deterministic prevention, and `hr-r-2` proves a SAFE GenLayer admission. No change, incident or settlement is claimed because no truthful qualifying event occurred during the review window.
