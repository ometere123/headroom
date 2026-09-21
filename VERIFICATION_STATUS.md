# Verification Status

## Canonical contract

The deployed Studionet contract `0x4d300dF9aCADC904DfC9473F0D970bd6CB1c122C` was finalized successfully by transaction `0x571288f46cef612de2ff24cf120a2ddeb922a3ce1e9b5200bb2c05668ee6b929`. Deployed source SHA-256 is `461fc74172e1d4a8a3e36d344280bc4e1cb22afd8ac44d9ea750138ee3954abe`, matching repository `contracts/headroom.py` at source commit `7aecd8f4312557de504de2709d04f646c102dce0`. Its schema is 10 views and 21 writes. Live `get_stats()` reports Studionet, chain 61999, balanced accounting, and no admin controls.

## Candidate checks

Record the results for the exact release commit here and in [review evidence](docs/REVIEW_EVIDENCE.md):

- Python 3.12.3 compile: PASS (`contracts/headroom.py`, all direct and integration test modules).
- GenVM validation: `genvm-linter==0.11.1rc2`; the reviewed exact seven E010 custom validator diagnostics remain the only accepted warnings.
- Direct Mode: PASS, 54 passed (`genlayer-test==0.29.2`, `genlayer-py==0.16.3`).
- `check_release.py`, `check_contract_patterns.py`, `check_frontend_surface.py`: PASS.
- Frontend SDK: exact `genlayer-js==1.1.8`; `npm run typecheck` and `npm run build`: PASS.
- GitHub Actions: pending candidate push.
- Vercel Production: existing project linked; four required Production variables confirmed; production deploy pending.

## Live protocol evidence

The deployment is verified. Covenant creation and subsequent protocol operations require a wallet signature from the user. Until those transactions are personally approved and successfully finalized, this repository makes no live claim for semantic admission, prevention, change preflight, incident measurement, exception examination, liability, challenge, settlement, or withdrawal.
